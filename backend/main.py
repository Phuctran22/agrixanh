"""
AgriXanh Backend - Entry Point (main.py) - Reloaded
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.api import auth, products, orders, inventory, payments, ai_vision, statistics, loyalty


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle: khởi động và tắt ứng dụng."""
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="AgriXanh API",
    description="🌿 Hệ thống thương mại điện tử nông sản tích hợp AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(ai_vision.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")
app.include_router(loyalty.router,    prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "🌿 AgriXanh API đang hoạt động!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "service": "AgriXanh Backend"}
