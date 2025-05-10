# FastAPI aur data validation modules import kiye gaye hain
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

# FastAPI application initialize kiya gaya
app = FastAPI()

# ✅ Yeh ek model hai jo request ke JSON data ko validate karega
# Real-world example: Product ya Item form fill karte waqt yeh structure use hoga
class Item(BaseModel):
    name: str  # item ka naam (required)
    description: str | None = None  # item ki detail (optional)
    price: float  # item ka price (required)

# ✅ Endpoint 1: Item ko ID ke zariye fetch karna
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,  # Required parameter (missing default value ka matlab yeh zaroori hai)
        title="The ID of the item",  # Swagger UI me help text
        description="A unique identifier for the item",
        ge=1  # Only allow ID >= 1
    )
):
    # Real-world example: E-commerce me kisi specific product ki detail fetch karna
    return {"item_id": item_id}

# ✅ Endpoint 2: Multiple items ko query parameters ke sath fetch karna
@app.get("/items/")
async def read_items(
    q: str | None = Query(
        None,  # Optional query string (search bar jaise)
        title="Query string",
        description="Query string for searching items",
        min_length=3,  # Kam az kam 3 characters
        max_length=50  # Zyada se zyada 50 characters
    ),
    skip: int = Query(0, ge=0),  # Pagination ke liye: kitne items skip karne hain
    limit: int = Query(10, le=100)  # Kitne items chahiye: max 100
):
    # Real-world example: Website par search aur pagination (e.g., page 2, 10 items per page)
    return {"q": q, "skip": skip, "limit": limit}

# ✅ Endpoint 3: Kisi item ko update karna, query aur JSON body ke sath
@app.put("/items/validated/{item_id}")
async def update_item(
    item_id: int = Path(..., title="Item ID", ge=1),  # Required aur >=1
    q: str | None = Query(None, min_length=3),  # Optional query string
    item: Item | None = Body(
        None,  # Optional JSON body
        description="Optional item data (JSON body)"
    )
):
    result = {"item_id": item_id}
    
    # Agar query string di gayi ho to result me shamil karein
    if q:
        result.update({"q": q})
    
    # Agar item object diya gaya ho to usay dict me convert karke shamil karein
    if item:
        result.update({"item": item.model_dump()})

    # Real-world example: Admin panel se product update karna (via form or API)
    return result
