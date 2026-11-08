"""
AgriXanh - API Products: Quản lý sản phẩm nông sản
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.core.database import get_db
from app.utils.mock_data import MOCK_PRODUCTS
from app.utils.helpers import generate_id, mongo_doc_to_dict
from datetime import datetime
import unicodedata
import re
import copy

router = APIRouter(prefix="/products", tags=["Products"])

_products_store = [dict(p) for p in MOCK_PRODUCTS]

def _get_current_store():
    global _products_store
    if len(_products_store) < len(MOCK_PRODUCTS):
        _products_store = [dict(p) for p in MOCK_PRODUCTS]
    return _products_store

_categories_store = ["Rau củ", "Trái cây", "Gia vị", "Thực phẩm khô", "Gạo & Ngũ cốc", "Nấm ăn"]

def remove_accents(input_str: str) -> str:
    if not input_str:
        return ""
    nfkd = unicodedata.normalize('NFKD', input_str)
    res = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return res.replace("đ", "d").replace("Đ", "D").lower()

def make_vietnamese_regex(search: str) -> str:
    if not search:
        return ""
    search_norm = remove_accents(search)
    replacements = {
        'a': '[aàáảãạăằắẳẵặâầấẩẫậ]',
        'e': '[eèéẻẽẹêềếểễệ]',
        'i': '[iìíỉĩị]',
        'o': '[oòóỏõọôồốổỗộơờớởỡợ]',
        'u': '[uùúủũụưừứửữự]',
        'y': '[yỳýỷỹỵ]',
        'd': '[dđ]',
    }
    escaped = ""
    for ch in search_norm:
        escaped += replacements.get(ch, re.escape(ch) if ch in r"\^$.|?*+()[]{}" else ch)
    return escaped

def _to_response(p: dict) -> dict:
    d = dict(p)
    d["id"] = d.pop("_id", d.get("id", ""))
    d.setdefault("farm_name", d.get("farm") or "Green Valley Farm")
    d.setdefault("origin", "Đà Lạt, Lâm Đồng")
    d.setdefault("ai_quality", "Loại 1 (Xuất sắc)")
    d.setdefault("ai_details", "Đạt chuẩn VietGAP, ngoại quan đều đẹp, độ tươi mới 96%.")
    d.setdefault("ai_color", "Màu sắc tự nhiên, đồng đều, đạt chuẩn độ chín sinh lý.")
    d.setdefault("ai_shape", "Hình dạng cân đối, kích thước đồng đều tiêu chuẩn.")
    d.setdefault("ai_surface", "Bề mặt căng bóng, không phát hiện sâu bệnh hoặc vết bầm dập.")
    d.setdefault("ai_confidence", 0.96)
    d.setdefault("freshness_score", 96)
    d.setdefault("rating", 4.8)
    d.setdefault("sold_count", 120)
    d.setdefault("stock_quantity", 50)
    d.setdefault("seller_id", "user_seller_001")
    d.setdefault("created_at", datetime.utcnow())
    return d


@router.get("", include_in_schema=False)
@router.get("/", summary="Lấy danh sách sản phẩm với bộ lọc & tìm kiếm nâng cao")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    seller_id: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    ai_quality: Optional[str] = None,
    origin: Optional[str] = None,
    in_stock: Optional[bool] = None,
    sort_by: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
):
    db = get_db()
    if db is not None:
        docs = await db.products.find({}).to_list(1000)
        items = [_to_response(mongo_doc_to_dict(d)) for d in docs]
    else:
        # Load fresh mock products
        items = [_to_response(p) for p in _get_current_store()]
        
    # Category filter
    if category and category not in ["All", "Tất cả"]:
        cat_norm = remove_accents(category)
        items = [
            p for p in items
            if cat_norm in remove_accents(p.get("category", ""))
            or (cat_norm == "rau cu" and ("rau" in remove_accents(p.get("category", "")) or "cu" in remove_accents(p.get("category", ""))))
        ]
        
    # Search keyword (Vietnamese diacritics + case insensitive)
    if search and search.strip():
        raw_q = search.strip().lower()
        norm_q = remove_accents(raw_q)
        def _match_search(p):
            text_corpus = " ".join([
                str(p.get("name", "")),
                str(p.get("description", "")),
                str(p.get("farm_name", "")),
                str(p.get("farm", "")),
                str(p.get("origin", "")),
                str(p.get("category", "")),
            ]).lower()
            text_norm = remove_accents(text_corpus)
            return raw_q in text_corpus or norm_q in text_norm

        items = [p for p in items if _match_search(p)]

    # Seller ID filter
    if seller_id:
        items = [p for p in items if p.get("seller_id") == seller_id]

    # Price range
    if min_price is not None:
        items = [p for p in items if p.get("price", 0) >= min_price]
    if max_price is not None:
        items = [p for p in items if p.get("price", 0) <= max_price]

    # AI Quality filter
    if ai_quality and ai_quality not in ["All", "Tất cả"]:
        q_norm = remove_accents(ai_quality)
        items = [p for p in items if q_norm in remove_accents(p.get("ai_quality", ""))]

    # Origin filter
    if origin and origin not in ["All", "Tất cả"]:
        orig_norm = remove_accents(origin)
        items = [p for p in items if orig_norm in remove_accents(p.get("origin", ""))]

    # In stock filter
    if in_stock:
        items = [p for p in items if p.get("stock_quantity", 0) > 0]

    # Sorting
    if sort_by == "popular":
        items.sort(key=lambda x: x.get("sold_count", 0), reverse=True)
    elif sort_by == "rating_desc":
        items.sort(key=lambda x: x.get("rating", 0.0), reverse=True)
    elif sort_by == "price_asc":
        items.sort(key=lambda x: x.get("price", 0.0))
    elif sort_by == "price_desc":
        items.sort(key=lambda x: x.get("price", 0.0), reverse=True)
    elif sort_by == "newest":
        items.sort(key=lambda x: x.get("created_at") or datetime.min, reverse=True)
    else:
        # Default sort: popularity / rating
        items.sort(key=lambda x: (x.get("rating", 0.0), x.get("sold_count", 0)), reverse=True)

    total = len(items)
    start = (page - 1) * per_page
    items = items[start:start + per_page]

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 1,
    }


@router.get("/categories", summary="Danh mục sản phẩm")
async def get_categories():
    db = get_db()
    if db is not None:
        cats = await db.categories.find().to_list(100)
        if cats:
            return {"categories": [c["name"] for c in cats]}
    return {"categories": _categories_store}


@router.get("/origins", summary="Danh sách xuất xứ / vùng trồng đối tác")
async def get_origins():
    origins = [
        "Đà Lạt, Lâm Đồng",
        "Mộc Châu, Sơn La",
        "Bảo Lộc, Lâm Đồng",
        "Hàm Yên, Tuyên Quang",
        "Bến Tre",
        "Vĩnh Long",
        "Sapa, Lào Cai",
        "Lý Sơn, Quảng Ngãi",
        "Sóc Trăng",
        "Bình Phước",
        "Cái Bè, Tiền Giang",
        "Bình Thuận",
    ]
    return {"origins": origins}


@router.get("/tags", summary="Gợi ý từ khóa tìm kiếm phổ biến")
async def get_tags():
    tags = [
        "Cà chua Đà Lạt",
        "Bơ sáp 034",
        "Dâu tây Hana",
        "Cam sành",
        "Bưởi da xanh",
        "Gạo ST25",
        "Cải Kale",
        "Nấm đùi gà",
        "Tỏi Lý Sơn",
        "Rau hữu cơ",
    ]
    return {"tags": tags}


@router.get("/featured", summary="Sản phẩm nổi bật tuần này")
async def get_featured(limit: int = 4):
    all_items = [_to_response(p) for p in _get_current_store()]
    all_items.sort(key=lambda x: x.get("sold_count", 0), reverse=True)
    return {"items": all_items[:limit]}


@router.get("/{product_id}/related", summary="Sản phẩm tương tự cùng danh mục")
async def get_related_products(product_id: str, limit: int = 4):
    store = _get_current_store()
    target = next((p for p in store if p.get("_id") == product_id or p.get("id") == product_id), None)
    all_items = [_to_response(p) for p in store if p.get("_id") != product_id and p.get("id") != product_id]
    if target:
        cat = target.get("category")
        same_cat = [p for p in all_items if p.get("category") == cat]
        if len(same_cat) >= limit:
            return {"items": same_cat[:limit]}
        remaining = [p for p in all_items if p not in same_cat]
        return {"items": (same_cat + remaining)[:limit]}
    return {"items": all_items[:limit]}


@router.get("/{product_id}", summary="Chi tiết sản phẩm")
async def get_product(product_id: str):
    db = get_db()
    if db is not None:
        doc = await db.products.find_one({"_id": product_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
        return _to_response(mongo_doc_to_dict(doc))
    store = _get_current_store()
    p = next((p for p in store if p.get("_id") == product_id or p.get("id") == product_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return _to_response(dict(p))


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, summary="Tạo sản phẩm mới (Người bán)")
async def create_product(data: dict):
    new_id = f"prod_{generate_id()}"
    new_prod = {
        "_id": new_id,
        "name": data.get("name", "Nông sản mới"),
        "description": data.get("description", ""),
        "price": float(data.get("price", 0)),
        "unit": data.get("unit", "kg"),
        "category": data.get("category", "Rau củ"),
        "origin": data.get("origin", "Việt Nam"),
        "image_url": data.get("image_url", ""),
        "seller_id": data.get("seller_id", "user_seller_001"),
        "stock_quantity": int(data.get("stock_quantity", 50)),
        "ai_quality": data.get("ai_quality", "Loại 1 (Xuất sắc)"),
        "ai_details": data.get("ai_details", "Độ tươi 95%, bề mặt sáng bóng không tì vết."),
        "ai_color": data.get("ai_color", "Màu sắc tươi mới, độ chín đồng nhất."),
        "ai_shape": data.get("ai_shape", "Kích thước tiêu chuẩn, không biến dạng."),
        "ai_surface": data.get("ai_surface", "Vỏ nhẵn mịn, không sâu bệnh."),
        "ai_confidence": float(data.get("ai_confidence", 0.95)),
        "rating": 5.0,
        "sold_count": 0,
        "created_at": datetime.utcnow(),
    }
    db = get_db()
    if db is not None:
        await db.products.insert_one(new_prod)
    else:
        _products_store.append(new_prod)
    return _to_response(dict(new_prod))


@router.put("/{product_id}", summary="Cập nhật sản phẩm")
async def update_product(product_id: str, data: dict):
    update_data = {k: v for k, v in data.items() if v is not None}
    update_data.pop("_id", None)
    update_data.pop("id", None)
    db = get_db()
    if db is not None:
        result = await db.products.update_one({"_id": product_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
        doc = await db.products.find_one({"_id": product_id})
        return _to_response(mongo_doc_to_dict(doc))
    else:
        for i, p in enumerate(_products_store):
            if p.get("_id") == product_id or p.get("id") == product_id:
                _products_store[i].update(update_data)
                return _to_response(dict(_products_store[i]))
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")


@router.delete("/{product_id}", summary="Xóa sản phẩm")
async def delete_product(product_id: str):
    db = get_db()
    if db is not None:
        result = await db.products.delete_one({"_id": product_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    else:
        global _products_store
        before = len(_products_store)
        _products_store = [p for p in _products_store if p.get("_id") != product_id]
        if len(_products_store) == before:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return {"message": "Đã xóa sản phẩm thành công"}
