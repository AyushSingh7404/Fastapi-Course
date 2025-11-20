from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name: Annotated[str, Field(min_length=2, max_length=50, title="Full Name", description="The full name of the patient", examples=["John Doe", "Jane Smith"])]
    age: Annotated[int, Field(gt=18, lt=65, description="Age must be between 18 and 65")]
    email: EmailStr
    website: AnyUrl
    weight: Annotated[float, Field(strict=True, gt=0, lt=100)]
    married: Annotated[bool, Field(description="Marital status of the patient")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_items=10)]
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Data updated successfully")

patient_info = {"name": "John Doe", "age": 30, "email": "john.doe@example.com", "website": "https://johndoe.com", "weight": 70.5, "married": False, "contact_details": {"phone": "123-456-7890"}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
