from pydantic import BaseModel, ValidationError

# Define a simple model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  # Optional field with default None

# Valid data
user_data = {"id": 1, "name": "Ramesha javed", "email": "Rameshajaved12gmail.com", "age": 23}
user = User(**user_data)
print(user) #object form
print(user.model_dump())  #dict form
print(user) 

try:
    invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
except ValidationError as e:
    print(e)