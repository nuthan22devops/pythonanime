import os
import asyncpg
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI(title="Order Service")
DATABASE_URL = os.environ["DATABASE_URL"]

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=30)
    item_id: int
    item_title: str
    quantity: int = Field(default=1, ge=1)
    total: float = Field(ge=0)

@app.get("/health")
async def health():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.close()
    return {"status": "UP", "service": "order-service"}

@app.post("/orders")
async def create_order(order: OrderRequest):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow("""
        INSERT INTO orders
        (customer_name, phone, item_id, item_title, quantity, total)
        VALUES ($1,$2,$3,$4,$5,$6)
        RETURNING id, customer_name, phone, item_id, item_title,
                  quantity, total::float, created_at
    """, order.customer_name, order.phone, order.item_id, order.item_title,
         order.quantity, order.total)
    await conn.close()
    return {"message": "Order placed successfully", "order": dict(row)}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow("""
        SELECT id, customer_name, phone, item_id, item_title,
               quantity, total::float, created_at
        FROM orders WHERE id=$1
    """, order_id)
    await conn.close()
    if not row:
        return {"message": "Order not found"}
    return dict(row)
