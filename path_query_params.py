from fastapi import FastAPI, HTTPException, Path, Query
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

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description=f"The field to sort patients by height, weight, or bmi"), order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", example="asc")):
    
    accepted_fields = ["height", "weight", "bmi"]
    if sort_by not in accepted_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field choose from {accepted_fields}")
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data