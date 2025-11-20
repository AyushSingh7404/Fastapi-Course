from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., description="Age of the patient", gt=18, lt=60)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., description="Height of the patient in mtrs", gt=0)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kgs", gt=0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=18, description="Age of the patient should be greater than 18")]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    return data


def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
    
    # load existing data
    data = load_data()
    
    # check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')
    
    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save the data back to the json file
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})

@app.put('/edit/{patient_id}')
def edit_patient(patient_id: str, patient_update: PatientUpdate):
    
    # load existing data
    data = load_data()
    
    # check if patient with given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    # update the patient details
    existing_patient_info = data[patient_id]
    
    updated_patient_info = patient_update.model_dump(exclude_unset=True)  # only get the fields that were provided in the request
    
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id  # add id back for creating pydantic object
    patient_pydantic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info
    
    
    # save the updated data back to the json file
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    # load existing data
    data = load_data()
    
    # check if patient with given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    # delete the patient
    del data[patient_id]
    
    # save the updated data back to the json file
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})