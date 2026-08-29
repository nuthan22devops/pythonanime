import os
import httpx

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Anime Store Frontend")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

ANIME_SERVICE_URL = os.environ["ANIME_SERVICE_URL"]
CHECKOUT_SERVICE_URL = os.environ["CHECKOUT_SERVICE_URL"]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
return templates.TemplateResponse(
"home.html",
{"request": request}
)

@app.get("/items", response_class=HTMLResponse)
async def items(request: Request):
async with httpx.AsyncClient(timeout=10) as client:
r = await client.get(f"{ANIME_SERVICE_URL}/items")
r.raise_for_status()

```
return templates.TemplateResponse(
    "items.html",
    {
        "request": request,
        "items": r.json()
    }
)
```

@app.get("/checkout/{item_id}", response_class=HTMLResponse)
async def checkout_page(request: Request, item_id: int):
async with httpx.AsyncClient(timeout=10) as client:
r = await client.get(
f"{ANIME_SERVICE_URL}/items/{item_id}"
)
r.raise_for_status()

```
return templates.TemplateResponse(
    "checkout.html",
    {
        "request": request,
        "item": r.json()
    }
)
```

@app.post("/checkout/{item_id}", response_class=HTMLResponse)
async def checkout(
request: Request,
item_id: int,
customer_name: str = Form(...),
phone: str = Form(...),
quantity: int = Form(1),
):
async with httpx.AsyncClient(timeout=10) as client:

```
    item_response = await client.get(
        f"{ANIME_SERVICE_URL}/items/{item_id}"
    )

    item_response.raise_for_status()

    item = item_response.json()

    order_response = await client.post(
        f"{CHECKOUT_SERVICE_URL}/checkout",
        json={
            "customer_name": customer_name,
            "phone": phone,
            "item_id": item["id"],
            "item_title": item["title"],
            "price": item["price"],
            "quantity": quantity
        }
    )

    order_response.raise_for_status()

    result = order_response.json()

order = result["order"]

return templates.TemplateResponse(
    "order.html",
    {
        "request": request,
        "order": order,
        "message": result["message"]
    }
)
```

@app.get("/health")
async def health():
return {
"status": "UP",
"service": "frontend-service"
}
