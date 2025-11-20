from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):
    
    name: str
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Data updated successfully")

patient_info = {"name": "John Doe", "age": 30, "weight": 70.5, "married": False, "contact_details": {"phone": "123-456-7890", "email": "john.doe@example.com"}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
