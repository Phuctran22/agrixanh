"""
AgriXanh - API Inventory: Quản lý kho hàng
"""
from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.utils.mock_data import MOCK_PRODUCTS
from app.utils.helpers import mongo_doc_to_dict
from datetime import datetime, timedelta

router = APIRouter(prefix="/inventory", tags=["Inventory"])

_inventory_store = [
    {
        "product_id": p["_id"],
        "product_name": p["name"],
        "current_stock": p["stock_quantity"],
        "min_stock_threshold": 10,
        "expiry_date": (datetime.utcnow() + timedelta(days=5 if p["stock_quantity"] < 10 else 30)),
        "last_updated": datetime.utcnow(),
    }
    for p in MOCK_PRODUCTS
]


@router.get("", include_in_schema=False)
@router.get("/", summary="Danh sách tồn kho")
async def get_inventory():
    db = get_db()
    if db is not None:
        cursor = db.products.find({}, {"_id": 1, "name": 1, "stock_quantity": 1})
        docs = await cursor.to_list(length=100)
        items = [
            {
                "product_id": str(d.get("_id")),
                "product_name": d.get("name"),
                "current_stock": d.get("stock_quantity", 0),
                "min_stock_threshold": 10,
                "last_updated": datetime.utcnow(),
            }
            for d in docs
        ]
        return {"items": items}
    return {"items": [dict(i) for i in _inventory_store]}


@router.get("/low-stock", summary="Sản phẩm sắp hết hàng")
async def get_low_stock():
    db = get_db()
    if db is not None:
        cursor = db.products.find({"stock_quantity": {"$lte": 10}})
        docs = await cursor.to_list(length=50)
        items = [mongo_doc_to_dict(d) for d in docs]
        return {"items": items, "count": len(items)}
    low = [i for i in _inventory_store if i["current_stock"] <= i["min_stock_threshold"]]
    return {"items": low, "count": len(low)}


@router.get("/expiring", summary="Sản phẩm sắp hết hạn (trong 7 ngày)")
async def get_expiring():
    threshold = datetime.utcnow() + timedelta(days=7)
    expiring = [
        i for i in _inventory_store
        if i.get("expiry_date") and i["expiry_date"] <= threshold
    ]
    return {"items": expiring, "count": len(expiring)}


@router.patch("/{product_id}/stock", summary="Cập nhật tồn kho")
async def update_stock(product_id: str, quantity: int):
    db = get_db()
    if db is not None:
        result = await db.products.update_one(
            {"_id": product_id},
            {"$set": {"stock_quantity": quantity}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    else:
        for i in _inventory_store:
            if i["product_id"] == product_id:
                i["current_stock"] = quantity
                i["last_updated"] = datetime.utcnow()
                return {"message": "Đã cập nhật tồn kho", "product_id": product_id, "new_stock": quantity}
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return {"message": "Đã cập nhật tồn kho", "product_id": product_id, "new_stock": quantity}
