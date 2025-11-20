from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/greet")
def greet():
    return {"message": "Hey! nice to meet you Ayush this side."}
