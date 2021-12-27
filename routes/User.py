import re
import pdfplumber
from fastapi import APIRouter, File, UploadFile
from models.User import user
#from models.UserCreditCard import userCreditCard
from config.db import conn
from schemas.user import serializeList

userRouter=APIRouter()

@userRouter.get('/')
async def findAllUsers():
    return serializeList(conn.local.user.find())

# @userRouter.post('/')
# async def SaveUser(cust:user):
#     conn.local.user.insert_one(dict(cust))
#     return serializeList(conn.local.user.find())

@userRouter.post('/pdf')
async def uploadFile(file:UploadFile = File(...)):

    with pdfplumber.open(file.file) as pdf:
        page=pdf.pages[0]
        text=page.extract_text()


    customer_re = re.compile(r'NAME')
    for line in text.split('\n'):
        if customer_re.match(line):
          customer=line.split()
    userName=customer[1]+" "+customer[2] 


    customer_re = re.compile(r'ACCOUNT NUMBER')
    for line in text.split('\n'):
        if customer_re.match(line):
            customer=line.split()
    userNumber=customer[2]+customer[3]+customer[4]+customer[5]

    payment_re = re.compile(r'Payment Due Date')
    for line in text.split('\n'):
        if payment_re.match(line):
            data=line.split()
            payment=data[3]+" "+data[4]+" "+data[5]


    conn.local.user.drop()
    
    allUsers=serializeList(conn.local.user.find())

    count = 0
    for item in allUsers:
        if(item["userAccNumber"]==userNumber):
            count+=1
    
    obj=user(userName=userName,userAccNumber=userNumber,userCredit=[],userPaymentDue=[])

    if(count==0):
        conn.local.user.insert_one(dict(obj))
    
    c=0

    Paymentcheck=serializeList(conn.local.user.find({"customerAccNumber":userNumber}))


    for item in Paymentcheck:
        if(payment in item["userPaymentDue"]):
            c+=1
        else:
            c=0
    if(c==0):
        conn.local.user.find_one_and_update({"userAccNumber":userNumber},{"$push":{"userPaymentDue":payment}},{"upsert":True})
        credits_re=re.compile(r'^\d{1,2} [A-Z].*')
        
        amount=""
        date="" 
        count=0
        
        for line in text.split('\n'):
            if credits_re.match(line):
                data=line.split()
                activity=""
                date=data[0]+data[1]+data[2]
                for i in range(4,len(data)):
                    if(data[i].find('$')):
                        activity+=data[i-1]+" "+data[i]
                    else:
                        amount=data[i]
                        if(count==0):
                            amount=float(data[i][1:])
                            count=0
                        
                conn.local.user.find_one_and_update({"userAccNumber":userNumber},{"$push":{"userCredit":{"date":date,"activity":activity,"amount":amount}}},{"upsert":True})
        return "Hi "+ userName+"!! Bank statement added successfully"
    else:
        return "Hi "+ userName+"!! Something went wrong, upload the correct file"
    




