from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age >60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients above 60 years of age')
        return model


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '73', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency_contact':'9876543210'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)