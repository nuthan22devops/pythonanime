# AnimeVerse — Python Microservices Demo

A simple anime shopping application built with **4 Python microservices + PostgreSQL**.

## Architecture

Browser
→ `frontend-service` (UI / gateway)
→ `anime-service` (catalog)
→ `checkout-service` (checkout)
→ `order-service` (order persistence)
→ PostgreSQL

### Services

| Service | Port | Responsibility |
|---|---:|---|
| frontend-service | 8080 | Homepage, item index, checkout and order-success UI |
| anime-service | 8001 | Anime catalog APIs |
| checkout-service | 8002 | Calculates total and calls order service |
| order-service | 8003 | Saves and retrieves orders |
| PostgreSQL | 5432 | Persistent data |

## Run

Prerequisite: Docker Desktop / Docker Engine + Docker Compose.

```bash
docker compose up --build
```

Open:

**http://localhost:8080**

## Flow

1. Homepage → `GET /`
2. Anime index → `GET /items`
3. Click **Buy Now**
4. Checkout → enter name, phone and quantity
5. Click **Place Order**
6. Frontend calls checkout-service
7. Checkout-service calculates total and calls order-service
8. Order-service stores the order in PostgreSQL
9. Success page displays **Order placed successfully!** and order ID

## Useful API checks

```bash
curl http://localhost:8001/items
curl http://localhost:8003/health
curl http://localhost:8002/health
```

This is intentionally simple for learning microservices, Docker Compose, REST APIs and PostgreSQL. For production, add authentication, API gateway/security, retries, service discovery, migrations, observability, secrets management and separate databases per service.
