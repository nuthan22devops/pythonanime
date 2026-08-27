import os
import asyncpg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Anime Catalog Service")
DATABASE_URL = os.environ["DATABASE_URL"]

@app.get("/health")
async def health():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.close()
    return {"status": "UP", "service": "anime-service"}

@app.get("/items")
async def items():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT id, title, description, price::float, image_url, category
        FROM anime_items ORDER BY id
    """)
    await conn.close()
    return [dict(r) for r in rows]

@app.get("/items/{item_id}")
async def item(item_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow("""
        SELECT id, title, description, price::float, image_url, category
        FROM anime_items WHERE id=$1
    """, item_id)
    await conn.close()
    if not row:
        raise HTTPException(404, "Anime item not found")
    return dict(row)
