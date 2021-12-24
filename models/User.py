from typing import List
from pydantic import BaseModel


class creditCardDetails(BaseModel):
    date:str
    activity:str
    amount:float
  

class user(BaseModel):
    userName:str
    userAccNumber:str   
    userCredit:List[creditCardDetails]
    userPaymentDue:list