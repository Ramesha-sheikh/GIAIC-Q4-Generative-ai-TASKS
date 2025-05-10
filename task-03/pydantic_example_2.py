from pydantic import BaseModel, EmailStr

# Define a nested model


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  # Built-in validator for email format
    addresses: list[Address]  # List of nested Address models


# Valid data with nested structure
user_data = {
    "id": 2,
    "name": "Ramesha javed",
    "email": "RaMESHAjaved1@example.com",
    "addresses": [
        {"street": "09 ", "city": "karachi", "zip_code": "001"},
        {"street": "04", "city": "lahore", "zip_code": "001"},
    ],
}
user = UserWithAddress.model_validate(user_data)
print(user.model_dump())