from pydantic import BaseModel

class Address(BaseModel):
  
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
  
    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city':'New Delhi', 'state':'Delhi', 'pin_code':'110001'}

address1 = Address(**address_dict)

patient_dict = {'name':'Nitish', 'gender':'Male', 'age':29, 'address': address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address.city)
print(patient1.address.pin_code)