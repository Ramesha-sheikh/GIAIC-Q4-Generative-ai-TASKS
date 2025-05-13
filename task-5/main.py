from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated

# FastAPI application initialize kiya ja raha hai
app = FastAPI()

# ----------------------- 1. Simple Dependency -----------------------

# Ye function ek simple static goal return karta hai
def get_goal():
    # Return kar raha hai aik simple dictionary jo goal ko specify karta hai
    return {"goal": "Learning AI with FastAPI"}

# '/goal' endpoint jo get_goal() function ko dependency ke tor par use karta hai
@app.get("/goal")
def read_goal(data: Annotated[dict, Depends(get_goal)]):
    # Is endpoint ko call karte waqt, 'get_goal' function se goal message milta hai
    return data


# ----------------------- 2. Dependency with Query Parameter -----------------------

# Ye function username query parameter ko accept karta hai
def get_user_goal(username: str = Query(..., description="Enter your username")):
    # Function user-specific goal ko return karta hai
    return {"username": username, "goal": "Mastering FastAPI"}

# '/user-goal' endpoint jo get_user_goal() function ko dependency ke tor par use karta hai
@app.get("/user-goal")
def read_user_goal(info: Annotated[dict, Depends(get_user_goal)]):
    # Query se mila hua username aur goal ko return karta hai
    return info


# ----------------------- 3. Login Dependency with Logic -----------------------

# Ye function login ko handle karta hai, username aur password ke saath
def login_check(username: str = Query(...), password: str = Query(...)):
    # Agar username aur password sahi hain to login successful message return karte hain
    if username == "admin" and password == "admin":
        return {"status": "Login Successful"}
    # Agar credentials galat hain to 401 Unauthorized error raise karte hain
    raise HTTPException(status_code=401, detail="Invalid Credentials")

# '/login' endpoint jo login_check() function ko dependency ke tor par use karta hai
@app.get("/login")
def login_status(auth: Annotated[dict, Depends(login_check)]):
    # Login ke response ko return karta hai, jo status message include karta hai
    return auth


# ----------------------- 4. Multiple Dependencies -----------------------

# Pehla dependency function, jo number mein 1 add karta hai
def add_one(value: int):
    # Function number mein 1 add karta hai aur return karta hai
    return value + 1

# Dusra dependency function, jo number mein 2 add karta hai
def add_two(value: int):
    # Function number mein 2 add karta hai aur return karta hai
    return value + 2

# '/calculate/{value}' endpoint, jo dono dependencies ko use karta hai
@app.get("/calculate/{value}")
def calculate_total(
    value: int, # Path parameter jo value ko accept karta hai
    result1: Annotated[int, Depends(add_one)], # Pehla dependency jo add_one() function ko call karega
    result2: Annotated[int, Depends(add_two)]  # Dosra dependency jo add_two() function ko call karega
):
    # Final result jo value, result1 aur result2 ko add karke calculate kiya jaata hai
    total = value + result1 + result2
    # Total ko return karte hain
    return {"total": total}


# ----------------------- 5. Class-Based Dependency with 404 Handling -----------------------

# Ye ek dictionary hai jo dummy data ko store karta hai
items = {
    "1": "FastAPI Tutorial",
    "2": "Dependency Injection Guide"
}

# Yeh ek class hai jo object ko fetch karti hai aur agar object na mile to 404 error raise karti hai
class GetItemOr404:
    def __init__(self, source: dict):
        self.source = source

    def __call__(self, item_id: str):
        # Source dictionary se item ko retrieve karte hain
        item = self.source.get(item_id)
        # Agar item nahi mila, to 404 error raise hota hai
        if not item:
            raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
        # Agar item mil gaya to usse return karte hain
        return item

# Class ka instance create kiya ja raha hai
item_dependency = GetItemOr404(items)

# '/items/{item_id}' endpoint, jo item_dependency ko dependency ke tor par use karta hai
@app.get("/items/{item_id}")
def read_item(item: Annotated[str, Depends(item_dependency)]):
    # Item ko return karte hain jo item_dependency ke through fetch hota hai
    return {"item": item}

