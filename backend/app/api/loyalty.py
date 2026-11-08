"""
AgriXanh – Loyalty Program Router (FastAPI)
Routes: /api/v1/loyalty/...  |  /api/v1/users/...
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.core.database import get_db
from app.models.loyalty import (
    AddressCreate, AddressUpdate, AddressResponse,
    ProfileUpdate, ProfileResponse,
    LoyaltyTransactionCreate, LoyaltyTransactionResponse, LoyaltySummary,
    RedeemRequest, RedeemResponse,
    PointSource, TierLevel,
    TIER_PERKS, EARN_RATE, REDEEM_RATE,
    compute_tier, compute_progress,
)
from app.utils.helpers import generate_id, mongo_doc_to_dict
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import copy

router = APIRouter(prefix="/loyalty", tags=["Loyalty & Account"])
security = HTTPBearer()

# ─────────────────────────── MOCK STORES (fallback khi không có MongoDB) ─────────

_users_store_ref = None          # will be filled lazily from auth module


def _get_users_store():
    """Lazy import để tránh circular dependency."""
    from app.api.auth import _users_store
    return _users_store


_addresses_store: list[dict] = []    # embedded addresses per user (mock)
_loyalty_store:   list[dict] = []    # loyalty_points collection (mock)


# ─────────────────────────── HELPERS ─────────────────────────────

def _require_user(credentials: HTTPAuthorizationCredentials) -> dict:
    """Decode JWT and return payload dict {sub, role}."""
    return decode_token(credentials.credentials)


async def _get_user_doc(user_id: str, db) -> dict:
    if db is not None:
        doc = await db.users.find_one({"_id": user_id})
        if doc:
            return mongo_doc_to_dict(doc)
    users = _get_users_store()
    user = next((u for u in users if u.get("_id") == user_id), None)
    if user:
        return dict(user)
    return None


async def _get_loyalty_doc(user_id: str, db) -> dict:
    """Get or create loyalty profile for a user."""
    if db is not None:
        doc = await db.loyalty_profiles.find_one({"user_id": user_id})
        if doc:
            return mongo_doc_to_dict(doc)
        # auto-create
        new_profile = {
            "_id": f"lp_{generate_id()}",
            "user_id": user_id,
            "total_points": 0,
            "total_spent": 0.0,
            "tier": TierLevel.bronze,
            "created_at": datetime.now(timezone.utc),
        }
        await db.loyalty_profiles.insert_one(new_profile)
        return mongo_doc_to_dict(new_profile)

    # Mock fallback
    doc = next((d for d in _loyalty_store if d["user_id"] == user_id), None)
    if doc:
        return dict(doc)
    new_profile = {
        "_id": f"lp_{generate_id()}",
        "user_id": user_id,
        "total_points": 0,
        "total_spent": 0.0,
        "tier": TierLevel.bronze,
        "created_at": datetime.now(timezone.utc),
    }
    _loyalty_store.append(new_profile)
    return dict(new_profile)


# ─────────────────────────── 1. PROFILE ──────────────────────────────────

@router.get("/profile", summary="Lấy hồ sơ cá nhân đầy đủ", response_model=ProfileResponse)
async def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()
    user = await _get_user_doc(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    uid = user.get("id") or user.get("_id")
    addresses = await _list_addresses_raw(uid, db)
    return ProfileResponse(
        id          = uid,
        email       = user["email"],
        full_name   = user.get("full_name", ""),
        phone       = user.get("phone", ""),
        birth_date  = user.get("birth_date"),
        avatar_url  = user.get("avatar_url", ""),
        role        = user.get("role", "customer"),
        is_active   = user.get("is_active", True),
        created_at  = user.get("created_at", datetime.now(timezone.utc)),
        addresses   = [AddressResponse(**a) for a in addresses],
    )


@router.put("/profile", summary="Cập nhật hồ sơ cá nhân")
async def update_profile(
    data: ProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()
    update_fields = {k: v for k, v in data.model_dump().items() if v is not None}

    if db is not None:
        await db.users.update_one({"_id": user_id}, {"$set": update_fields})
        user = await _get_user_doc(user_id, db)
    else:
        users = _get_users_store()
        for i, u in enumerate(users):
            if u.get("_id") == user_id or u.get("id") == user_id:
                users[i].update(update_fields)
                user = dict(users[i])
                break
        else:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    uid = user.get("id") or user.get("_id")
    addresses = await _list_addresses_raw(uid, db)
    return ProfileResponse(
        id          = uid,
        email       = user["email"],
        full_name   = user.get("full_name", ""),
        phone       = user.get("phone", ""),
        birth_date  = user.get("birth_date"),
        avatar_url  = user.get("avatar_url", ""),
        role        = user.get("role", "customer"),
        is_active   = user.get("is_active", True),
        created_at  = user.get("created_at", datetime.now(timezone.utc)),
        addresses   = [AddressResponse(**a) for a in addresses],
    )


@router.post("/profile/avatar", summary="Upload ảnh đại diện (base64 URL)")
async def upload_avatar(
    avatar_url: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Nhận avatar_url (có thể là URL Cloudinary, S3, hay data:image base64).
    Trong production hãy gọi API upload lên cloud storage trước, rồi lưu URL.
    """
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    if db is not None:
        await db.users.update_one({"_id": user_id}, {"$set": {"avatar_url": avatar_url}})
    else:
        users = _get_users_store()
        for i, u in enumerate(users):
            if u.get("_id") == user_id or u.get("id") == user_id:
                users[i]["avatar_url"] = avatar_url
                break

    return {"message": "Cập nhật ảnh đại diện thành công", "avatar_url": avatar_url}


# ─────────────────────────── 2. SỔ ĐỊA CHỈ ──────────────────────────────

async def _list_addresses_raw(user_id: str, db) -> list[dict]:
    """Internal helper – returns list of address dicts."""
    if db is not None:
        cursor = db.addresses.find({"user_id": user_id})
        docs = await cursor.to_list(length=20)
        return [mongo_doc_to_dict(d) for d in docs]
    return [dict(a) for a in _addresses_store if a["user_id"] == user_id]


@router.get("", include_in_schema=False)
@router.get("/addresses", summary="Danh sách địa chỉ")
async def list_addresses(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()
    items = await _list_addresses_raw(user_id, db)
    return {"items": items}


@router.post("/addresses", status_code=201, summary="Thêm địa chỉ mới")
async def add_address(
    data: AddressCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    new_addr = {
        "_id":            f"addr_{generate_id()}",
        "id":             f"addr_{generate_id()}",
        "user_id":        user_id,
        "recipient_name": data.recipient_name,
        "phone":          data.phone,
        "address_line":   data.address_line,
        "ward":           data.ward or "",
        "district":       data.district or "",
        "province":       data.province or "",
        "is_default":     data.is_default,
        "created_at":     datetime.now(timezone.utc),
    }
    new_addr["id"] = new_addr["_id"]

    if data.is_default:
        # Bỏ is_default cho các địa chỉ khác
        if db is not None:
            await db.addresses.update_many(
                {"user_id": user_id, "is_default": True},
                {"$set": {"is_default": False}},
            )
        else:
            for a in _addresses_store:
                if a["user_id"] == user_id:
                    a["is_default"] = False

    if db is not None:
        await db.addresses.insert_one(copy.deepcopy(new_addr))
    else:
        _addresses_store.append(new_addr)

    return AddressResponse(
        id             = new_addr["id"],
        recipient_name = new_addr["recipient_name"],
        phone          = new_addr["phone"],
        address_line   = new_addr["address_line"],
        ward           = new_addr["ward"],
        district       = new_addr["district"],
        province       = new_addr["province"],
        is_default     = new_addr["is_default"],
    )


@router.put("/addresses/{address_id}", summary="Cập nhật địa chỉ")
async def update_address(
    address_id: str,
    data: AddressUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()
    update_fields = {k: v for k, v in data.model_dump().items() if v is not None}

    if data.is_default:
        if db is not None:
            await db.addresses.update_many(
                {"user_id": user_id, "is_default": True},
                {"$set": {"is_default": False}},
            )
        else:
            for a in _addresses_store:
                if a["user_id"] == user_id:
                    a["is_default"] = False

    if db is not None:
        result = await db.addresses.update_one(
            {"_id": address_id, "user_id": user_id},
            {"$set": update_fields},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")
        doc = await db.addresses.find_one({"_id": address_id})
        return mongo_doc_to_dict(doc)
    else:
        for i, a in enumerate(_addresses_store):
            if (a.get("_id") == address_id or a.get("id") == address_id) and a["user_id"] == user_id:
                _addresses_store[i].update(update_fields)
                return dict(_addresses_store[i])
        raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")


@router.delete("/addresses/{address_id}", summary="Xóa địa chỉ")
async def delete_address(
    address_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    if db is not None:
        result = await db.addresses.delete_one({"_id": address_id, "user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")
    else:
        before = len(_addresses_store)
        _addresses_store[:] = [
            a for a in _addresses_store
            if not ((a.get("_id") == address_id or a.get("id") == address_id) and a["user_id"] == user_id)
        ]
        if len(_addresses_store) == before:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")

    return {"message": "Đã xóa địa chỉ"}


@router.patch("/addresses/{address_id}/default", summary="Đặt địa chỉ mặc định")
async def set_default_address(
    address_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    if db is not None:
        await db.addresses.update_many({"user_id": user_id}, {"$set": {"is_default": False}})
        result = await db.addresses.update_one(
            {"_id": address_id, "user_id": user_id},
            {"$set": {"is_default": True}},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")
    else:
        found = False
        for a in _addresses_store:
            if a["user_id"] == user_id:
                a["is_default"] = (a.get("_id") == address_id or a.get("id") == address_id)
                if a["is_default"]:
                    found = True
        if not found:
            raise HTTPException(status_code=404, detail="Không tìm thấy địa chỉ")

    return {"message": "Đã đặt địa chỉ mặc định"}


# ─────────────────────────── 3. LOYALTY PROGRAM ──────────────────────────

@router.get("/points", summary="Tổng quan điểm & hạng thành viên")
async def get_loyalty_summary(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    lp = await _get_loyalty_doc(user_id, db)
    total_points = lp.get("total_points", 0)
    total_spent  = float(lp.get("total_spent", 0))
    tier         = compute_tier(total_spent)
    progress     = compute_progress(total_spent, tier)
    perks        = TIER_PERKS[tier]

    # 10 giao dịch gần nhất
    if db is not None:
        cursor = db.loyalty_transactions.find({"user_id": user_id}).sort("created_at", -1).limit(10)
        txn_docs = await cursor.to_list(length=10)
        recent_txns = [mongo_doc_to_dict(d) for d in txn_docs]
    else:
        recent_txns = sorted(
            [t for t in _loyalty_store if isinstance(t, dict) and t.get("user_id") == user_id and "points" in t],
            key=lambda x: x.get("created_at", datetime.min),
            reverse=True,
        )[:10]

    return {
        "user_id":       user_id,
        "total_points":  total_points,
        "total_spent":   total_spent,
        "tier":          tier,
        "tier_label":    perks["label"],
        "tier_emoji":    perks["emoji"],
        "tier_color":    perks["color"],
        "progress_pct":  progress["progress_pct"],
        "spent_to_next": progress.get("spent_to_next"),
        "perks":         perks,
        "recent_txns":   recent_txns,
    }


@router.post("/points/earn", status_code=201, summary="Cộng điểm tích lũy")
async def earn_points(
    data: LoyaltyTransactionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Endpoint nội bộ – gọi sau khi đơn hàng hoàn tất hoặc user đánh giá sản phẩm.
    source: 'purchase' → tính từ ref order amount  |  'review' → cộng cố định 5 điểm.
    """
    payload = _require_user(credentials)
    caller_id = payload["sub"]
    # Cho phép admin hoặc chính user đó
    if caller_id != data.user_id and payload.get("role") not in ("admin", "seller"):
        raise HTTPException(status_code=403, detail="Không có quyền")

    db = get_db()
    lp = await _get_loyalty_doc(data.user_id, db)
    current_points = lp.get("total_points", 0)
    current_spent  = float(lp.get("total_spent", 0))

    # Tính điểm theo nguồn
    points_to_add = data.points
    if data.source == PointSource.purchase and data.points == 0:
        # Auto-calc: yêu cầu caller truyền order_amount trong ref_id field
        points_to_add = 0   # sẽ tính ở order hook
    if data.source == PointSource.review:
        points_to_add = max(data.points, 5)   # tối thiểu 5 điểm cho review

    # Nhân hệ số theo tier
    tier  = compute_tier(current_spent)
    multi = TIER_PERKS[tier]["bonus_points"]
    if data.source == PointSource.purchase:
        points_to_add = int(points_to_add * multi)

    new_balance = current_points + points_to_add
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=365)

    txn = {
        "_id":          f"txn_{generate_id()}",
        "user_id":      data.user_id,
        "source":       data.source,
        "points":       points_to_add,
        "ref_id":       data.ref_id,
        "note":         data.note,
        "balance_after": new_balance,
        "expires_at":   expires_at,
        "created_at":   now,
    }

    # Cập nhật tổng chi tiêu nếu là mua hàng
    new_spent = current_spent
    if data.source == PointSource.purchase and data.ref_id:
        # ref_id truyền order amount vào note hoặc tách riêng; giả sử data.note có amount
        try:
            order_amount = float(data.note or 0)
            new_spent += order_amount
        except (ValueError, TypeError):
            pass

    if db is not None:
        await db.loyalty_transactions.insert_one(dict(txn))
        await db.loyalty_profiles.update_one(
            {"user_id": data.user_id},
            {"$set": {"total_points": new_balance, "total_spent": new_spent}},
            upsert=True,
        )
    else:
        _loyalty_store.append(txn)
        for lp_item in _loyalty_store:
            if isinstance(lp_item, dict) and lp_item.get("user_id") == data.user_id and "tier" in lp_item:
                lp_item["total_points"] = new_balance
                lp_item["total_spent"]  = new_spent
                break

    return {**txn, "message": f"Đã cộng {points_to_add} điểm", "new_balance": new_balance}


@router.post("/points/earn-order", status_code=201, summary="Tích điểm từ đơn hàng (tự động)")
async def earn_points_from_order(
    order_id: str,
    order_amount: float,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Gọi sau khi order status = 'delivered'. Tự tính điểm theo tỷ lệ EARN_RATE.
    Công thức: floor(order_amount / EARN_RATE) × tier_bonus_multiplier
    """
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    lp = await _get_loyalty_doc(user_id, db)
    tier  = compute_tier(float(lp.get("total_spent", 0)))
    multi = TIER_PERKS[tier]["bonus_points"]

    base_points  = int(order_amount // EARN_RATE)
    final_points = max(1, int(base_points * multi))
    new_total    = int(lp.get("total_points", 0)) + final_points
    new_spent    = float(lp.get("total_spent",  0)) + order_amount

    now        = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=365)
    txn = {
        "_id":           f"txn_{generate_id()}",
        "user_id":       user_id,
        "source":        PointSource.purchase,
        "points":        final_points,
        "ref_id":        order_id,
        "note":          f"Mua hàng #{order_id} – {int(order_amount):,}đ × {multi}x",
        "balance_after": new_total,
        "expires_at":    expires_at,
        "created_at":    now,
    }

    if db is not None:
        await db.loyalty_transactions.insert_one(dict(txn))
        new_tier = compute_tier(new_spent)
        await db.loyalty_profiles.update_one(
            {"user_id": user_id},
            {"$set": {"total_points": new_total, "total_spent": new_spent, "tier": new_tier}},
            upsert=True,
        )
    else:
        _loyalty_store.append(txn)
        for lp_item in _loyalty_store:
            if isinstance(lp_item, dict) and lp_item.get("user_id") == user_id and "tier" in lp_item:
                lp_item["total_points"] = new_total
                lp_item["total_spent"]  = new_spent
                lp_item["tier"]         = compute_tier(new_spent)
                break

    return {
        "order_id":     order_id,
        "points_earned": final_points,
        "new_balance":   new_total,
        "new_spent":     new_spent,
        "new_tier":      compute_tier(new_spent),
        "message":       f"🎉 Tích lũy {final_points} điểm từ đơn hàng {order_id}",
    }


@router.post("/points/redeem", summary="Tính toán đổi điểm (preview)")
async def redeem_preview(
    data: RedeemRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Preview (chưa trừ điểm) – dùng để hiển thị giá trị giảm trước khi xác nhận thanh toán.
    Để thực sự trừ điểm, gọi /redeem/confirm sau khi tạo order thành công.
    """
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    lp = await _get_loyalty_doc(user_id, db)
    available = int(lp.get("total_points", 0))
    points_to_use = min(data.points_to_use, available)

    discount = points_to_use * REDEEM_RATE
    discount = min(discount, data.order_amount * 0.50)   # Tối đa giảm 50% hóa đơn
    actual_points_used = int(discount / REDEEM_RATE)

    return RedeemResponse(
        original_amount  = data.order_amount,
        points_used      = actual_points_used,
        discount_amount  = discount,
        final_amount     = data.order_amount - discount,
        remaining_points = available - actual_points_used,
    )


@router.post("/points/redeem/confirm", status_code=201, summary="Xác nhận đổi điểm")
async def redeem_confirm(
    data: RedeemRequest,
    order_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    lp = await _get_loyalty_doc(user_id, db)
    available = int(lp.get("total_points", 0))
    points_to_use = min(data.points_to_use, available)
    discount = points_to_use * REDEEM_RATE
    discount = min(discount, data.order_amount * 0.50)
    actual_used = int(discount / REDEEM_RATE)

    if actual_used <= 0:
        raise HTTPException(status_code=400, detail="Không đủ điểm để đổi thưởng")

    new_balance = available - actual_used
    now = datetime.now(timezone.utc)
    txn = {
        "_id":           f"txn_{generate_id()}",
        "user_id":       user_id,
        "source":        PointSource.redeem,
        "points":        -actual_used,
        "ref_id":        order_id,
        "note":          f"Đổi điểm đơn #{order_id} – giảm {int(discount):,}đ",
        "balance_after": new_balance,
        "expires_at":    None,
        "created_at":    now,
    }

    if db is not None:
        await db.loyalty_transactions.insert_one(dict(txn))
        await db.loyalty_profiles.update_one(
            {"user_id": user_id},
            {"$set": {"total_points": new_balance}},
        )
    else:
        _loyalty_store.append(txn)
        for lp_item in _loyalty_store:
            if isinstance(lp_item, dict) and lp_item.get("user_id") == user_id and "tier" in lp_item:
                lp_item["total_points"] = new_balance
                break

    return {
        "order_id":       order_id,
        "points_used":    actual_used,
        "discount_amount": discount,
        "final_amount":   data.order_amount - discount,
        "remaining_points": new_balance,
        "message":         f"✅ Đã dùng {actual_used} điểm, giảm {int(discount):,}đ",
    }


@router.get("/tiers", summary="Thông tin các cấp hạng thành viên")
async def get_tiers():
    """Trả về đầy đủ thông tin các hạng thành viên để hiển thị trên Frontend."""
    return {
        "earn_rate":   EARN_RATE,
        "redeem_rate": REDEEM_RATE,
        "tiers": [
            {
                "level":       tier.value,
                "min_spent":   min_spent,
                **TIER_PERKS[tier],
            }
            for tier, min_spent in [
                (TierLevel.bronze,  0),
                (TierLevel.silver,  2_000_000),
                (TierLevel.gold,    5_000_000),
                (TierLevel.diamond, 15_000_000),
            ]
        ],
    }


@router.get("/transactions", summary="Lịch sử giao dịch điểm")
async def list_transactions(
    limit: int = 20,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload = _require_user(credentials)
    user_id = payload["sub"]
    db = get_db()

    if db is not None:
        cursor = db.loyalty_transactions.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        items = [mongo_doc_to_dict(d) for d in docs]
    else:
        items = sorted(
            [t for t in _loyalty_store if isinstance(t, dict) and t.get("user_id") == user_id and "points" in t],
            key=lambda x: x.get("created_at", datetime.min),
            reverse=True,
        )[:limit]

    return {"items": items, "total": len(items)}
