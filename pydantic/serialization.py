from pydantic import BaseModel

class Address(BaseModel):
  
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
  
    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city':'New Delhi', 'state':'Delhi', 'pin_code':'110001'}

address1 = Address(**address_dict)

patient_dict = {'name':'Nitish', 'age':29, 'address': address1}

patient1 = Patient(**patient_dict)

# temp = patient1.model_dump()

# temp = patient1.model_dump_json()

# temp = patient1.model_dump(include={'name', 'address'}, exclude={'address': {'pin_code'}})

temp = patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))