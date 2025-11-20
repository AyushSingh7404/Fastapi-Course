from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return {"message": "This is Ayush's FastAPI application."}

@app.get("/greet")
def about():
    return {"message": "Hey! nice to meet you you can see what is the json data here."}

@app.get("/data")
def data():
    data = load_data()
    return data