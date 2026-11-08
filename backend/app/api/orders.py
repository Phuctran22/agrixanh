"""
AgriXanh - API Orders: Đơn hàng, Giỏ hàng, Giao hàng & Quản lý tồn kho
Triển khai đầy đủ theo Master Prompt:
- Kiểm tra tồn kho và trừ kho nguyên tử (Atomic Stock Deduction)
- Tích hợp Sổ địa chỉ & Điểm tích lũy (Loyalty Points)
- Snapshot giá tại thời điểm chốt đơn
- Quản lý vòng đời đơn hàng cho Buyer và Seller
"""
from fastapi import APIRouter, HTTPException, Query, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timezone
import copy

from app.models.schemas import (
    OrderCreate, OrderResponse, OrderStatus, PaymentMethod, PaymentStatus,
    OrderPreviewRequest, OrderPreviewResponse, CartItem
)
from app.models.loyalty import (
    TierLevel, TIER_PERKS, TIER_THRESHOLDS, EARN_RATE, REDEEM_RATE,
    PointSource, compute_tier
)
from app.core.database import get_db
from app.core.security import decode_token
from app.utils.mock_data import MOCK_ORDERS, MOCK_PRODUCTS
from app.utils.helpers import generate_id, mongo_doc_to_dict

router = APIRouter(prefix="/orders", tags=["Orders"])
security = HTTPBearer(auto_error=False)

# In-memory store fallback khi không có MongoDB
_orders_store: List[dict] = [dict(o) for o in MOCK_ORDERS]

STATUS_LABEL = {
    "pending": "Chờ xác nhận",
    "confirmed": "Đã xác nhận",
    "picking": "Đang chuẩn bị hàng",
    "shipping": "Đang giao hàng",
    "delivered": "Giao thành công",
    "cancelled": "Đã hủy",
    "returned": "Hoàn trả",
}


def _get_current_products_store():
    """Lấy danh sách sản phẩm mock đồng bộ với products router."""
    from app.api.products import _get_current_store
    try:
        return _get_current_store()
    except Exception:
        return MOCK_PRODUCTS


def _get_current_loyalty_store():
    """Lấy danh sách điểm thưởng mock đồng bộ với loyalty router."""
    from app.api.loyalty import _loyalty_store
    return _loyalty_store


def get_current_user_payload(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    """Trích xuất token người dùng nếu có."""
    if credentials and credentials.credentials:
        try:
            return decode_token(credentials.credentials)
        except Exception:
            return None
    return None


async def _get_user_loyalty(user_id: str, db) -> dict:
    """Lấy thông tin Loyalty của User (Tier, Points, Spent)."""
    if db is not None:
        doc = await db.loyalty_profiles.find_one({"user_id": user_id})
        if doc:
            return mongo_doc_to_dict(doc)
        return {"user_id": user_id, "total_points": 0, "total_spent": 0.0, "tier": "bronze"}
    
    l_store = _get_current_loyalty_store()
    doc = next((d for d in l_store if isinstance(d, dict) and d.get("user_id") == user_id and "total_points" in d), None)
    if doc:
        return dict(doc)
    return {"user_id": user_id, "total_points": 1500, "total_spent": 2500000.0, "tier": "silver"}


def _to_resp(o: dict) -> dict:
    d = dict(o)
    d["id"] = d.pop("_id", d.get("id", ""))
    now = datetime.now(timezone.utc)
    d.setdefault("created_at", now)
    d.setdefault("updated_at", now)
    d.setdefault("customer_id", "user_cust_001")
    d.setdefault("customer_name", "Khách hàng")
    d.setdefault("phone", "0901234567")
    d.setdefault("seller_id", "user_seller_001")
    d.setdefault("subtotal", float(d.get("total_amount", 0.0)))
    d.setdefault("discount_amount", 0.0)
    d.setdefault("points_used", 0)
    d.setdefault("shipping_fee", 0.0)
    d.setdefault("total_amount", float(d.get("subtotal", 0.0)))
    d.setdefault("payment_method", "cod")
    d.setdefault("payment_status", "pending")
    d.setdefault("order_status", "pending")
    d.setdefault("note", "")
    d.setdefault("points_awarded", False)
    d["status_label"] = STATUS_LABEL.get(d.get("order_status", ""), "Chờ xác nhận")
    return d


# ==============================================================================
# 1. PREVIEW ORDER (Tính toán giá, Ưu đãi Loyalty, Phí vận chuyển)
# ==============================================================================
@router.post("/preview", response_model=OrderPreviewResponse, summary="Tính toán giá trị đơn hàng (Preview)")
async def preview_order(
    data: OrderPreviewRequest,
    user_payload: Optional[dict] = Depends(get_current_user_payload),
):
    """
    Tính toán chi phí đơn hàng, tự động áp dụng ưu đãi:
    - Miễn phí vận chuyển nếu đạt hạng Gold/Diamond hoặc đơn hàng >= 300.000đ.
    - Tính giảm giá từ Điểm tích lũy (Loyalty Points) theo tỉ lệ 1 điểm = 100đ, tối đa 50% đơn hàng.
    """
    db = get_db()
    user_id = (user_payload.get("sub") if user_payload else None) or "user_cust_001"
    
    # 1. Tính Tạm tính (Subtotal)
    subtotal = 0.0
    for item in data.items:
        subtotal += float(item.unit_price) * int(item.quantity)

    # 2. Lấy thông tin Loyalty của khách hàng
    loyalty_doc = await _get_user_loyalty(user_id, db)
    tier_str = loyalty_doc.get("tier", "bronze")
    available_points = int(loyalty_doc.get("total_points", 0))

    try:
        tier_enum = TierLevel(tier_str)
    except Exception:
        tier_enum = TierLevel.bronze
    
    tier_perks = TIER_PERKS.get(tier_enum, TIER_PERKS[TierLevel.bronze])
    
    # 3. Tính phí vận chuyển (Free ship cho Gold/Diamond hoặc đơn hàng >= 300k)
    is_free_shipping = tier_perks.get("free_shipping", False) or (subtotal >= 300_000)
    shipping_fee = 0.0 if is_free_shipping else 25_000.0

    # 4. Tính điểm Loyalty giảm giá
    max_discount_allowed = subtotal * 0.50  # tối đa giảm 50% hóa đơn
    max_points_applicable = int(max_discount_allowed / REDEEM_RATE)
    
    points_to_use = max(0, min(data.points_to_use or 0, available_points, max_points_applicable))
    discount_amount = float(points_to_use * REDEEM_RATE)

    # 5. Tổng thanh toán cuối cùng
    final_total = max(0.0, subtotal - discount_amount + shipping_fee)

    # 6. Dự tính điểm thưởng nhận được sau khi hoàn thành
    bonus_multiplier = float(tier_perks.get("bonus_points", 1.0))
    points_to_earn = int((final_total / EARN_RATE) * bonus_multiplier)

    return OrderPreviewResponse(
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        discount_amount=discount_amount,
        points_used=points_to_use,
        final_total=final_total,
        available_points=available_points,
        points_to_earn=points_to_earn,
        user_tier=tier_enum.value,
        is_free_shipping=is_free_shipping,
    )


# ==============================================================================
# 2. CREATE ORDER (Khởi tạo đơn hàng, Trừ kho nguyên tử, Trừ điểm Loyalty)
# ==============================================================================
@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Tạo đơn hàng mới")
async def create_order(
    data: OrderCreate,
    user_payload: Optional[dict] = Depends(get_current_user_payload),
):
    if not data.items or len(data.items) == 0:
        raise HTTPException(status_code=400, detail="Giỏ hàng đang trống, không thể tạo đơn hàng")

    db = get_db()
    user_id = (user_payload.get("sub") if user_payload else None) or data.customer_id or "user_cust_001"
    now = datetime.now(timezone.utc)

    # 1. Kiểm tra tồn kho sản phẩm (Inventory Stock Validation)
    if db is not None:
        for item in data.items:
            prod = await db.products.find_one({"_id": item.product_id})
            if not prod:
                raise HTTPException(status_code=400, detail=f"Sản phẩm '{item.product_name}' không tồn tại hoặc đã ngừng kinh doanh")
            current_stock = prod.get("stock_quantity", 0)
            if current_stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Nông sản '{item.product_name}' hiện chỉ còn {current_stock} kg trong kho, không đủ đáp ứng số lượng bạn chọn ({item.quantity} kg)."
                )
    else:
        products_store = _get_current_products_store()
        for item in data.items:
            prod = next((p for p in products_store if p.get("_id") == item.product_id or p.get("id") == item.product_id), None)
            if prod:
                current_stock = prod.get("stock_quantity", 0)
                if current_stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Nông sản '{item.product_name}' hiện chỉ còn {current_stock} kg trong kho."
                    )

    # 2. Tính toán lại Subtotal và Snapshot giá thực tế
    subtotal = 0.0
    processed_items = []
    primary_seller_id = "user_seller_001"

    for item in data.items:
        unit_price = float(item.unit_price)
        subtotal += unit_price * item.quantity
        seller = item.seller_id or primary_seller_id
        if seller:
            primary_seller_id = seller
        
        processed_items.append({
            "product_id": item.product_id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "unit_price": unit_price,
            "seller_id": seller,
            "unit": item.unit or "kg",
            "image_url": item.image_url or "",
        })

    # 3. Tính toán Loyalty Discount & Phí vận chuyển
    loyalty_doc = await _get_user_loyalty(user_id, db)
    tier_str = loyalty_doc.get("tier", "bronze")
    available_points = int(loyalty_doc.get("total_points", 0))

    try:
        tier_enum = TierLevel(tier_str)
    except Exception:
        tier_enum = TierLevel.bronze
    
    tier_perks = TIER_PERKS.get(tier_enum, TIER_PERKS[TierLevel.bronze])
    is_free_shipping = tier_perks.get("free_shipping", False) or (subtotal >= 300_000)
    shipping_fee = 0.0 if is_free_shipping else 25_000.0

    max_discount_allowed = subtotal * 0.50
    max_points_applicable = int(max_discount_allowed / REDEEM_RATE)
    points_to_use = max(0, min(data.points_to_use or 0, available_points, max_points_applicable))
    discount_amount = float(points_to_use * REDEEM_RATE)
    final_total = max(0.0, subtotal - discount_amount + shipping_fee)

    # 4. Trừ tồn kho nguyên tử (Atomic Stock Deduction)
    if db is not None:
        for item in data.items:
            await db.products.update_one(
                {"_id": item.product_id},
                {"$inc": {"stock_quantity": -item.quantity, "sold_count": item.quantity}}
            )
    else:
        products_store = _get_current_products_store()
        for item in data.items:
            for p in products_store:
                if p.get("_id") == item.product_id or p.get("id") == item.product_id:
                    p["stock_quantity"] = max(0, p.get("stock_quantity", 0) - item.quantity)
                    p["sold_count"] = p.get("sold_count", 0) + item.quantity
                    break

    # 5. Trừ điểm Loyalty nếu có sử dụng
    new_order_id = f"ord_{generate_id()}"
    if points_to_use > 0:
        new_balance = max(0, available_points - points_to_use)
        redeem_txn = {
            "_id": f"txn_{generate_id()}",
            "user_id": user_id,
            "source": PointSource.redeem.value,
            "points": -points_to_use,
            "ref_id": new_order_id,
            "note": f"Đổi điểm đơn hàng #{new_order_id[:8]} – Giảm {int(discount_amount):,}đ",
            "balance_after": new_balance,
            "expires_at": None,
            "created_at": now,
        }
        if db is not None:
            await db.loyalty_transactions.insert_one(redeem_txn)
            await db.loyalty_profiles.update_one(
                {"user_id": user_id},
                {"$set": {"total_points": new_balance}}
            )
        else:
            l_store = _get_current_loyalty_store()
            l_store.append(redeem_txn)
            for item_lp in l_store:
                if isinstance(item_lp, dict) and item_lp.get("user_id") == user_id and "tier" in item_lp:
                    item_lp["total_points"] = new_balance
                    break

    # 6. Chuẩn hóa địa chỉ giao hàng
    shipping_addr_val = data.shipping_address
    if isinstance(shipping_addr_val, dict):
        shipping_addr_obj = shipping_addr_val
    else:
        shipping_addr_obj = {
            "recipient_name": data.customer_name or "Khách hàng",
            "phone": data.phone or "0901234567",
            "address_line": str(shipping_addr_val),
        }

    # 7. Khởi tạo Document Đơn hàng
    new_order = {
        "_id": new_order_id,
        "customer_id": user_id,
        "customer_name": data.customer_name or shipping_addr_obj.get("recipient_name") or "Khách hàng AgriXanh",
        "phone": data.phone or shipping_addr_obj.get("phone") or "0901234567",
        "seller_id": primary_seller_id,
        "items": processed_items,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "points_used": points_to_use,
        "shipping_fee": shipping_fee,
        "total_amount": final_total,
        "shipping_address": shipping_addr_obj,
        "payment_method": data.payment_method.value if hasattr(data.payment_method, "value") else str(data.payment_method),
        "payment_status": "pending",
        "order_status": "pending",
        "note": data.note or "",
        "points_awarded": False,
        "created_at": now,
        "updated_at": now,
    }

    if db is not None:
        await db.orders.insert_one(new_order)
    else:
        _orders_store.insert(0, new_order)

    return _to_resp(new_order)


# ==============================================================================
# 3. GET ORDERS (Danh sách đơn hàng cho Buyer, Seller và Admin)
# ==============================================================================
@router.get("", include_in_schema=False)
@router.get("/", summary="Danh sách đơn hàng")
async def get_orders(
    customer_id: Optional[str] = None,
    seller_id: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user_payload: Optional[dict] = Depends(get_current_user_payload),
):
    db = get_db()
    query: Dict[str, Any] = {}

    # Nếu người dùng có token, tự động giới hạn phạm vi truy vấn phù hợp
    if user_payload:
        role = user_payload.get("role", "customer")
        uid = user_payload.get("sub")
        if role == "customer":
            query["customer_id"] = uid
        elif role == "seller":
            # Seller chỉ xem đơn có hàng của seller đó
            if not seller_id:
                query["seller_id"] = uid

    if customer_id:
        query["customer_id"] = customer_id
    if seller_id:
        query["seller_id"] = seller_id
    if status and status.lower() != "all":
        query["order_status"] = status.lower()

    if db is not None:
        cursor = db.orders.find(query).sort("created_at", -1).skip((page - 1) * per_page).limit(per_page)
        docs = await cursor.to_list(length=per_page)
        total = await db.orders.count_documents(query)
        items = [_to_resp(mongo_doc_to_dict(d)) for d in docs]
    else:
        filtered = [dict(o) for o in _orders_store]
        if "customer_id" in query:
            filtered = [o for o in filtered if o.get("customer_id") == query["customer_id"]]
        if "seller_id" in query:
            filtered = [o for o in filtered if o.get("seller_id") == query["seller_id"]]
        if "order_status" in query:
            filtered = [o for o in filtered if o.get("order_status") == query["order_status"]]
        
        total = len(filtered)
        start = (page - 1) * per_page
        items = [_to_resp(o) for o in filtered[start:start + per_page]]

    return {"items": items, "total": total, "page": page, "per_page": per_page}


# ==============================================================================
# 4. GET SINGLE ORDER
# ==============================================================================
@router.get("/{order_id}", summary="Chi tiết đơn hàng")
async def get_order(order_id: str):
    db = get_db()
    if db is not None:
        doc = await db.orders.find_one({"_id": order_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
        return _to_resp(mongo_doc_to_dict(doc))
    
    o = next((o for o in _orders_store if o.get("_id") == order_id or o.get("id") == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return _to_resp(dict(o))


# ==============================================================================
# 5. UPDATE STATUS & CANCEL ORDER
# ==============================================================================
@router.patch("/{order_id}/status", summary="Cập nhật trạng thái đơn hàng")
async def update_order_status(
    order_id: str,
    new_status: OrderStatus,
    user_payload: Optional[dict] = Depends(get_current_user_payload),
):
    db = get_db()
    now = datetime.now(timezone.utc)
    
    # 1. Tìm đơn hàng hiện tại
    current_order = None
    if db is not None:
        doc = await db.orders.find_one({"_id": order_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
        current_order = mongo_doc_to_dict(doc)
    else:
        current_order = next((dict(o) for o in _orders_store if o.get("_id") == order_id or o.get("id") == order_id), None)
        if not current_order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

    prev_status = current_order.get("order_status")
    status_str = new_status.value if hasattr(new_status, "value") else str(new_status)

    update_fields: Dict[str, Any] = {
        "order_status": status_str,
        "updated_at": now,
    }

    # 2. Xử lý khi ĐƠN HOÀN THÀNH (delivered): Cộng điểm tích lũy & cập nhật doanh số chi tiêu
    if status_str == "delivered" and not current_order.get("points_awarded"):
        customer_id = current_order.get("customer_id") or "user_cust_001"
        total_amount = float(current_order.get("total_amount", 0.0))
        
        loyalty_doc = await _get_user_loyalty(customer_id, db)
        current_spent = float(loyalty_doc.get("total_spent", 0.0))
        current_points = int(loyalty_doc.get("total_points", 0))
        
        tier_str = loyalty_doc.get("tier", "bronze")
        try:
            tier_enum = TierLevel(tier_str)
        except Exception:
            tier_enum = TierLevel.bronze
        bonus_multiplier = float(TIER_PERKS.get(tier_enum, {}).get("bonus_points", 1.0))
        
        points_earned = int((total_amount / EARN_RATE) * bonus_multiplier)
        new_points_balance = current_points + points_earned
        new_total_spent = current_spent + total_amount
        new_tier = compute_tier(new_total_spent).value

        earn_txn = {
            "_id": f"txn_{generate_id()}",
            "user_id": customer_id,
            "source": PointSource.purchase.value,
            "points": points_earned,
            "ref_id": order_id,
            "note": f"Tích lũy từ đơn #{order_id[:8]} – {int(total_amount):,}đ × {bonus_multiplier}x",
            "balance_after": new_points_balance,
            "expires_at": None,
            "created_at": now,
        }

        if db is not None:
            await db.loyalty_transactions.insert_one(earn_txn)
            await db.loyalty_profiles.update_one(
                {"user_id": customer_id},
                {"$set": {"total_points": new_points_balance, "total_spent": new_total_spent, "tier": new_tier}},
                upsert=True
            )
        else:
            l_store = _get_current_loyalty_store()
            l_store.append(earn_txn)
            for item_lp in l_store:
                if isinstance(item_lp, dict) and item_lp.get("user_id") == customer_id and "tier" in item_lp:
                    item_lp["total_points"] = new_points_balance
                    item_lp["total_spent"] = new_total_spent
                    item_lp["tier"] = new_tier
                    break

        update_fields["points_awarded"] = True
        update_fields["payment_status"] = "paid"

    # 3. Xử lý khi ĐƠN BỊ HỦY (cancelled): Hoàn trả số lượng tồn kho & Hoàn trả điểm đã đổi
    elif status_str == "cancelled" and prev_status != "cancelled":
        # Hoàn tồn kho
        for item in current_order.get("items", []):
            pid = item.get("product_id")
            qty = item.get("quantity", 0)
            if db is not None:
                await db.products.update_one(
                    {"_id": pid},
                    {"$inc": {"stock_quantity": qty, "sold_count": -qty}}
                )
            else:
                for p in _get_current_products_store():
                    if p.get("_id") == pid or p.get("id") == pid:
                        p["stock_quantity"] = p.get("stock_quantity", 0) + qty
                        p["sold_count"] = max(0, p.get("sold_count", 0) - qty)
                        break

        # Hoàn điểm nếu có sử dụng
        points_used = current_order.get("points_used", 0)
        if points_used > 0:
            customer_id = current_order.get("customer_id") or "user_cust_001"
            loyalty_doc = await _get_user_loyalty(customer_id, db)
            refund_balance = int(loyalty_doc.get("total_points", 0)) + points_used
            refund_txn = {
                "_id": f"txn_{generate_id()}",
                "user_id": customer_id,
                "source": PointSource.bonus.value,
                "points": points_used,
                "ref_id": order_id,
                "note": f"Hoàn điểm từ đơn hủy #{order_id[:8]}",
                "balance_after": refund_balance,
                "created_at": now,
            }
            if db is not None:
                await db.loyalty_transactions.insert_one(refund_txn)
                await db.loyalty_profiles.update_one(
                    {"user_id": customer_id},
                    {"$set": {"total_points": refund_balance}}
                )
            else:
                l_store = _get_current_loyalty_store()
                l_store.append(refund_txn)
                for item_lp in l_store:
                    if isinstance(item_lp, dict) and item_lp.get("user_id") == customer_id and "tier" in item_lp:
                        item_lp["total_points"] = refund_balance
                        break

    # 4. Ghi nhận cập nhật vào Database
    if db is not None:
        await db.orders.update_one({"_id": order_id}, {"$set": update_fields})
        doc = await db.orders.find_one({"_id": order_id})
        return _to_resp(mongo_doc_to_dict(doc))
    else:
        for i, o in enumerate(_orders_store):
            if o.get("_id") == order_id or o.get("id") == order_id:
                _orders_store[i].update(update_fields)
                return _to_resp(dict(_orders_store[i]))

    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")


@router.post("/{order_id}/cancel", summary="Khách hàng hủy đơn hàng")
async def cancel_order(
    order_id: str,
    user_payload: Optional[dict] = Depends(get_current_user_payload),
):
    db = get_db()
    current_order = None
    if db is not None:
        doc = await db.orders.find_one({"_id": order_id})
        if doc:
            current_order = mongo_doc_to_dict(doc)
    else:
        current_order = next((dict(o) for o in _orders_store if o.get("_id") == order_id or o.get("id") == order_id), None)

    if not current_order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

    # Chỉ cho phép hủy khi đơn còn ở trạng thái pending hoặc confirmed
    if current_order.get("order_status") not in ["pending", "confirmed"]:
        raise HTTPException(
            status_code=400,
            detail="Đơn hàng đã được xuất kho hoặc đang giao, không thể tự hủy. Vui lòng liên hệ hỗ trợ AgriXanh."
        )

    return await update_order_status(order_id, OrderStatus.cancelled, user_payload)
