from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/prediction")
async def get_prediction():
    foo = ['You will have success at work',
           'You will meet love',
           'You will meet an important person',
           'You will be caught in the mushroom rain',
           'You win the lottery']
    print(random.choice(foo))
    return {"message": random.choice(foo)}
