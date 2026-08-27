import os
import httpx
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI(title="Checkout Service")
ORDER_SERVICE_URL = os.environ["ORDER_SERVICE_URL"]

class CheckoutRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=30)
    item_id: int
    item_title: str
    price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)

@app.get("/health")
async def health():
    return {"status": "UP", "service": "checkout-service"}

@app.post("/checkout")
async def checkout(data: CheckoutRequest):
    total = round(data.price * data.quantity, 2)
    payload = {
        "customer_name": data.customer_name,
        "phone": data.phone,
        "item_id": data.item_id,
        "item_title": data.item_title,
        "quantity": data.quantity,
        "total": total
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(f"{ORDER_SERVICE_URL}/orders", json=payload)
        response.raise_for_status()
        return response.json()
