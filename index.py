from fastapi import FastAPI
from routes.User import userRouter

app=FastAPI()
app.include_router(userRouter)
