"""
AgriXanh - Hàm tiện ích chung
"""
from datetime import datetime
from typing import Any, Dict
import uuid


def generate_id() -> str:
    """Tạo ID ngẫu nhiên."""
    return str(uuid.uuid4())[:8]


def format_price(amount: float) -> str:
    """Định dạng tiền VNĐ."""
    return f"{amount:,.0f} ₫"


def mongo_doc_to_dict(doc: Any) -> Dict:
    """Chuyển MongoDB document sang dict, đổi _id thành id."""
    if doc is None:
        return None
    if isinstance(doc, dict):
        result = {}
        for k, v in doc.items():
            if k == "_id":
                result["id"] = str(v)
            elif isinstance(v, datetime):
                result[k] = v
            else:
                result[k] = v
        return result
    return doc


def paginate(data: list, page: int = 1, per_page: int = 10) -> dict:
    """Phân trang dữ liệu."""
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": data[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
    }
