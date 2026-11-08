"""
AgriXanh - API Payments: Thanh toán
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import PaymentMethod, PaymentStatus
from app.core.database import get_db
from app.utils.helpers import generate_id, mongo_doc_to_dict
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["Payments"])

_payments_store = [
    {
        "_id": "pay_001",
        "order_id": "ord_001",
        "amount": 100000,
        "method": "cod",
        "status": "pending",
        "transaction_id": None,
        "created_at": datetime.utcnow(),
    },
    {
        "_id": "pay_002",
        "order_id": "ord_002",
        "amount": 45000,
        "method": "momo",
        "status": "paid",
        "transaction_id": "MOMO_TXN_123456",
        "created_at": datetime.utcnow(),
    },
]


class PaymentCreate(BaseModel):
    order_id: str
    amount: float
    method: PaymentMethod


@router.get("", include_in_schema=False)
@router.get("/", summary="Danh sách giao dịch")
async def get_payments():
    db = get_db()
    if db is not None:
        cursor = db.payments.find({}).sort("created_at", -1)
        docs = await cursor.to_list(length=100)
        return {"items": [mongo_doc_to_dict(d) for d in docs]}
    return {"items": [dict(p) for p in _payments_store]}


@router.get("/{payment_id}", summary="Chi tiết giao dịch")
async def get_payment(payment_id: str):
    db = get_db()
    if db is not None:
        doc = await db.payments.find_one({"_id": payment_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")
        return mongo_doc_to_dict(doc)
    p = next((p for p in _payments_store if p.get("_id") == payment_id or p.get("id") == payment_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")
    return dict(p)


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, summary="Tạo giao dịch thanh toán")
async def create_payment(data: PaymentCreate):
    new_id = f"pay_{generate_id()}"
    payment = {
        "_id": new_id,
        "order_id": data.order_id,
        "amount": data.amount,
        "method": data.method.value,
        "status": "pending",
        "transaction_id": None,
        "created_at": datetime.utcnow(),
        "payment_url": None,
    }
    # Simulate payment gateway URL generation
    if data.method == PaymentMethod.vnpay:
        payment["payment_url"] = f"https://sandbox.vnpayment.vn/pay?amount={int(data.amount)}&order={data.order_id}"
    elif data.method == PaymentMethod.momo:
        payment["payment_url"] = f"https://test-payment.momo.vn/pay?amount={int(data.amount)}&ref={new_id}"
    elif data.method == PaymentMethod.zalopay:
        payment["payment_url"] = f"https://sandbox.zalopay.vn/pay?amount={int(data.amount)}&ref={new_id}"

    db = get_db()
    if db is not None:
        await db.payments.insert_one(payment)
    else:
        _payments_store.append(payment)
    return mongo_doc_to_dict(dict(payment))


@router.patch("/{payment_id}/confirm", summary="Xác nhận thanh toán thành công")
async def confirm_payment(payment_id: str, transaction_id: str = "MOCK_TXN"):
    db = get_db()
    update = {"status": "paid", "transaction_id": transaction_id}
    if db is not None:
        result = await db.payments.update_one({"_id": payment_id}, {"$set": update})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")
        doc = await db.payments.find_one({"_id": payment_id})
        if doc and doc.get("order_id"):
            await db.orders.update_one({"_id": doc["order_id"]}, {"$set": {"payment_status": "paid"}})
        return {"message": "Xác nhận thanh toán thành công", **mongo_doc_to_dict(doc)}
    else:
        for p in _payments_store:
            if p.get("_id") == payment_id or p.get("id") == payment_id:
                p.update(update)
                return {"message": "Xác nhận thanh toán thành công", **p}
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")

