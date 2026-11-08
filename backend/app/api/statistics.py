"""
AgriXanh - API Statistics: Thống kê & Dashboard
"""
from fastapi import APIRouter, Query
from app.core.database import get_db
from app.utils.mock_data import MOCK_ORDERS, MOCK_PRODUCTS
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/statistics", tags=["Statistics"])


def _generate_revenue_chart():
    """Tạo dữ liệu biểu đồ doanh thu 7 ngày gần nhất."""
    labels = []
    values = []
    orders_count = []
    for i in range(6, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        labels.append(day.strftime("%d/%m"))
        values.append(random.randint(500000, 3000000))
        orders_count.append(random.randint(5, 30))
    return {"labels": labels, "revenue": values, "orders": orders_count}


def _generate_monthly_revenue():
    """Tạo dữ liệu biểu đồ doanh thu 6 tháng."""
    months = ["T5", "T6", "T7", "T8", "T9", "T10"]
    return {
        "labels": months,
        "revenue": [random.randint(20000000, 80000000) for _ in months],
    }


@router.get("/dashboard", summary="Dashboard tổng quan")
async def get_dashboard():
    db = get_db()
    if db is not None:
        total_orders = await db.orders.count_documents({})
        total_products = await db.products.count_documents({})
        total_customers = await db.users.count_documents({"role": "customer"})
        low_stock = await db.products.count_documents({"stock_quantity": {"$lte": 10}})
    else:
        total_orders = len(MOCK_ORDERS)
        total_products = len(MOCK_PRODUCTS)
        total_customers = 3
        low_stock = sum(1 for p in MOCK_PRODUCTS if p.get("stock_quantity", 0) <= 10)

    return {
        "total_revenue": 12580000,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_customers": total_customers,
        "low_stock_count": low_stock,
        "revenue_change": 18.5,
        "orders_change": 12.3,
        "customers_change": 8.7,
        "revenue_chart": _generate_revenue_chart(),
        "monthly_revenue": _generate_monthly_revenue(),
        "top_products": [
            {"name": "Cà rốt baby", "sold": 450, "revenue": 20250000, "quality": "Loại 1"},
            {"name": "Cà chua đà lạt", "sold": 320, "revenue": 11200000, "quality": "Loại 1"},
            {"name": "Dưa leo mini", "sold": 210, "revenue": 6300000, "quality": "Loại 1"},
            {"name": "Xà lách romaine", "sold": 180, "revenue": 4500000, "quality": "Đạt chuẩn"},
            {"name": "Ớt chuông đỏ", "sold": 130, "revenue": 7150000, "quality": "Đạt chuẩn"},
        ],
        "quality_distribution": {
            "Loại 1": 55,
            "Loại 2": 25,
            "Đạt chuẩn": 15,
            "Không đạt": 5,
        },
        "order_status_distribution": {
            "pending": 8,
            "shipping": 15,
            "delivered": 77,
        },
    }


@router.get("/revenue", summary="Thống kê doanh thu")
async def get_revenue(
    period: str = Query("week", description="week | month | year")
):
    if period == "week":
        data = _generate_revenue_chart()
    elif period == "month":
        data = _generate_monthly_revenue()
    else:
        data = {
            "labels": [f"Q{i}" for i in range(1, 5)],
            "revenue": [random.randint(150000000, 300000000) for _ in range(4)],
        }
    return {"period": period, "data": data}


@router.get("/seller/{seller_id}", summary="Thống kê hiệu quả kinh doanh của gian hàng người bán")
async def get_seller_statistics(seller_id: str):
    return {
        "seller_id": seller_id,
        "total_revenue": 8640000,
        "total_orders": 24,
        "completed_orders": 21,
        "cancelled_orders": 1,
        "active_products": 6,
        "success_rate": 95.5,
        "revenue_growth": 16.2,
        "revenue_chart": _generate_revenue_chart(),
        "top_selling": [
            {"name": "Cà chua cherry Đà Lạt", "sold": 165, "revenue": 5775000, "grade": "Loại 1 (Xuất sắc)"},
            {"name": "Dưa leo baby Hữu cơ", "sold": 98, "revenue": 2940000, "grade": "Loại 1 (Xuất sắc)"},
            {"name": "Xà lách thủy canh", "sold": 75, "revenue": 1875000, "grade": "Đạt chuẩn VietGAP"},
        ]
    }
