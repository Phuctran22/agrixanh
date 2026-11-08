"""
AgriXanh - Loyalty Program Models (Pydantic Schemas)

Design Decision – Addresses Storage:
  Embedded (mảng `addresses` trong User document) được chọn vì:
  - Địa chỉ của 1 user hiếm khi > 10 entry → không có vấn đề về kích thước document.
  - Luôn được truy vấn cùng với User (profile page), tránh extra round-trip (JOIN).
  - Thay đổi thường xuyên cùng user nên embed giữ tính toàn vẹn dữ liệu.
  Collection riêng phù hợp hơn nếu địa chỉ được chia sẻ giữa nhiều entity (B2B scenarios).
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


# ─────────────────────────── TIER ───────────────────────────

class TierLevel(str, Enum):
    bronze   = "bronze"    # Đồng   – 0       ≤ spent < 2,000,000
    silver   = "silver"    # Bạc    – 2M      ≤ spent < 5,000,000
    gold     = "gold"      # Vàng   – 5M      ≤ spent < 15,000,000
    diamond  = "diamond"   # Kim Cương – 15M+


TIER_THRESHOLDS: dict[TierLevel, int] = {
    TierLevel.bronze:  0,
    TierLevel.silver:  2_000_000,
    TierLevel.gold:    5_000_000,
    TierLevel.diamond: 15_000_000,
}

TIER_PERKS: dict[TierLevel, dict] = {
    TierLevel.bronze: {
        "label":            "Đồng",
        "emoji":            "🥉",
        "color":            "#CD7F32",
        "free_shipping":    False,
        "priority_support": False,
        "cashback_rate":    0.0,      # phần trăm hoàn tiền thêm
        "bonus_points":     1.0,      # hệ số nhân điểm tích lũy
        "exclusive_deals":  False,
        "next_tier":        "silver",
        "next_at":          2_000_000,
    },
    TierLevel.silver: {
        "label":            "Bạc",
        "emoji":            "🥈",
        "color":            "#9EA5AD",
        "free_shipping":    False,
        "priority_support": False,
        "cashback_rate":    2.0,
        "bonus_points":     1.2,
        "exclusive_deals":  False,
        "next_tier":        "gold",
        "next_at":          5_000_000,
    },
    TierLevel.gold: {
        "label":            "Vàng",
        "emoji":            "🥇",
        "color":            "#F59E0B",
        "free_shipping":    True,
        "priority_support": False,
        "cashback_rate":    5.0,
        "bonus_points":     1.5,
        "exclusive_deals":  True,
        "next_tier":        "diamond",
        "next_at":          15_000_000,
    },
    TierLevel.diamond: {
        "label":            "Kim Cương",
        "emoji":            "💎",
        "color":            "#6366F1",
        "free_shipping":    True,
        "priority_support": True,
        "cashback_rate":    10.0,
        "bonus_points":     2.0,
        "exclusive_deals":  True,
        "next_tier":        None,
        "next_at":          None,
    },
}

# Quy đổi điểm
EARN_RATE  = 10_000   # 10.000 VNĐ → 1 điểm
REDEEM_RATE = 100      # 1 điểm → 100 VNĐ giảm trừ


# ─────────────────────────── ADDRESS ───────────────────────────

class AddressCreate(BaseModel):
    recipient_name: str = Field(..., min_length=2, max_length=100)
    phone:          str = Field(..., min_length=9, max_length=15)
    address_line:   str = Field(..., min_length=5, max_length=300)
    ward:           Optional[str] = ""
    district:       Optional[str] = ""
    province:       Optional[str] = ""
    is_default:     bool = False


class AddressUpdate(BaseModel):
    recipient_name: Optional[str] = None
    phone:          Optional[str] = None
    address_line:   Optional[str] = None
    ward:           Optional[str] = None
    district:       Optional[str] = None
    province:       Optional[str] = None
    is_default:     Optional[bool] = None


class AddressResponse(AddressCreate):
    id: str


# ─────────────────────────── PROFILE ───────────────────────────

class ProfileUpdate(BaseModel):
    full_name:  Optional[str] = None
    phone:      Optional[str] = None
    birth_date: Optional[str] = None   # "YYYY-MM-DD"
    avatar_url: Optional[str] = None


class ProfileResponse(BaseModel):
    id:          str
    email:       EmailStr
    full_name:   str
    phone:       Optional[str] = ""
    birth_date:  Optional[str] = None
    avatar_url:  Optional[str] = ""
    role:        str
    is_active:   bool
    created_at:  datetime
    addresses:   List[AddressResponse] = []


# ─────────────────────────── LOYALTY POINT TRANSACTION ───────────────────────────

class PointSource(str, Enum):
    purchase = "purchase"   # cộng điểm khi mua hàng
    review   = "review"     # cộng điểm khi đánh giá
    redeem   = "redeem"     # trừ điểm khi đổi thưởng
    expire   = "expire"     # điểm hết hạn bị trừ
    bonus    = "bonus"      # cộng thưởng từ admin


class LoyaltyTransactionCreate(BaseModel):
    user_id:    str
    source:     PointSource
    points:     int           # dương = cộng, âm = trừ
    ref_id:     Optional[str] = None   # order_id / review_id
    note:       Optional[str] = None


class LoyaltyTransactionResponse(LoyaltyTransactionCreate):
    id:         str
    balance_after: int
    expires_at: Optional[datetime] = None
    created_at: datetime


# ─────────────────────────── LOYALTY SUMMARY ───────────────────────────

class LoyaltySummary(BaseModel):
    user_id:        str
    total_points:   int             # điểm còn hiệu lực
    total_spent:    float           # tổng chi tiêu (VNĐ)
    tier:           TierLevel
    tier_info:      dict
    points_to_next: Optional[int] = None   # điểm cần tích để lên hạng
    spent_to_next:  Optional[float] = None
    progress_pct:   float = 0.0    # % tiến trình đến hạng tiếp theo (0-100)
    perks:          dict
    recent_txns:    List[LoyaltyTransactionResponse] = []


# ─────────────────────────── REDEEM CALCULATION ───────────────────────────

class RedeemRequest(BaseModel):
    order_amount:   float
    points_to_use:  int


class RedeemResponse(BaseModel):
    original_amount:    float
    points_used:        int
    discount_amount:    float
    final_amount:       float
    remaining_points:   int


# ─────────────────────────── HELPERS ───────────────────────────

def compute_tier(total_spent: float) -> TierLevel:
    """Xác định hạng thành viên theo tổng chi tiêu."""
    if total_spent >= TIER_THRESHOLDS[TierLevel.diamond]:
        return TierLevel.diamond
    if total_spent >= TIER_THRESHOLDS[TierLevel.gold]:
        return TierLevel.gold
    if total_spent >= TIER_THRESHOLDS[TierLevel.silver]:
        return TierLevel.silver
    return TierLevel.bronze


def compute_progress(total_spent: float, tier: TierLevel) -> dict:
    """Tính % tiến trình và khoảng cách đến hạng tiếp theo."""
    perks = TIER_PERKS[tier]
    next_at = perks.get("next_at")
    if next_at is None:                     # đã là Diamond
        return {"progress_pct": 100.0, "spent_to_next": None}
    current_floor = TIER_THRESHOLDS[tier]
    gap   = next_at - current_floor
    done  = total_spent - current_floor
    pct   = min(100.0, round(done / gap * 100, 1)) if gap > 0 else 100.0
    return {
        "progress_pct":  pct,
        "spent_to_next": max(0.0, next_at - total_spent),
    }
