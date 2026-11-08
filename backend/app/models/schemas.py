"""
AgriXanh - Pydantic Models (MongoDB schemas)
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union, Dict, Any
from datetime import datetime
from enum import Enum


# ============ ENUMS ============
class UserRole(str, Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    picking = "picking"
    shipping = "shipping"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"


class PaymentMethod(str, Enum):
    cod = "cod"
    vnpay = "vnpay"
    momo = "momo"
    zalopay = "zalopay"


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"


class AIQuality(str, Enum):
    grade1 = "Loại 1"
    grade2 = "Loại 2"
    grade3 = "Loại 3"
    passed = "Đạt chuẩn"
    failed = "Không đạt chuẩn"


# ============ USER ============
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: UserRole = UserRole.customer


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(UserBase):
    id: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime


# ============ PRODUCT ============
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    unit: str = "kg"
    category: str
    origin: Optional[str] = ""
    image_url: Optional[str] = ""
    seller_id: Optional[str] = ""


class ProductCreate(ProductBase):
    stock_quantity: int = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None


class ProductResponse(ProductBase):
    id: str
    stock_quantity: int
    ai_quality: Optional[str] = None
    rating: float = 0.0
    sold_count: int = 0
    created_at: datetime


# ============ CART & ORDER ============
class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    seller_id: Optional[str] = ""
    unit: Optional[str] = "kg"
    image_url: Optional[str] = ""


class ShippingAddressDetails(BaseModel):
    recipient_name: Optional[str] = ""
    phone: Optional[str] = ""
    address_line: Optional[str] = ""
    ward: Optional[str] = ""
    district: Optional[str] = ""
    province: Optional[str] = ""


class OrderCreate(BaseModel):
    items: List[CartItem]
    shipping_address: Union[str, Dict[str, Any]]
    payment_method: PaymentMethod = PaymentMethod.cod
    points_to_use: Optional[int] = 0
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = ""


class OrderPreviewRequest(BaseModel):
    items: List[CartItem]
    points_to_use: Optional[int] = 0
    shipping_address: Optional[Union[str, Dict[str, Any]]] = None


class OrderPreviewResponse(BaseModel):
    subtotal: float
    shipping_fee: float
    discount_amount: float
    points_used: int
    final_total: float
    available_points: int
    points_to_earn: int
    user_tier: str
    is_free_shipping: bool


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: Optional[str] = ""
    phone: Optional[str] = ""
    seller_id: Optional[str] = ""
    items: List[CartItem]
    subtotal: float
    discount_amount: float = 0.0
    points_used: int = 0
    shipping_fee: float = 0.0
    total_amount: float
    shipping_address: Union[str, Dict[str, Any]]
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    order_status: OrderStatus
    note: Optional[str] = ""
    status_label: Optional[str] = ""
    points_awarded: Optional[bool] = False
    created_at: datetime
    updated_at: datetime


# ============ INVENTORY ============
class InventoryItem(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    min_stock_threshold: int = 10
    expiry_date: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# ============ AI RESULT ============
class AIAnalysisResult(BaseModel):
    product_name: str
    quality_grade: AIQuality
    confidence: float
    details: str
    recommendations: List[str] = []
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


# ============ STATISTICS ============
class RevenueStats(BaseModel):
    period: str
    total_revenue: float
    total_orders: int
    avg_order_value: float


class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_products: int
    total_customers: int
    low_stock_count: int
    recent_orders: list = []
    revenue_chart: list = []
    top_products: list = []


# ============ TOKEN ============
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
