from fastapi import FastAPI
import time


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}