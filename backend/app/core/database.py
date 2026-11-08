"""
AgriXanh - Kết nối MongoDB (với fallback mock khi không có MongoDB)
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    """Kết nối MongoDB."""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
        await client.admin.command("ping")
        db = client[settings.DB_NAME]
        logger.info(f"✅ Kết nối MongoDB thành công: {settings.DB_NAME}")
        await seed_mock_data()
    except Exception as e:
        logger.warning(f"⚠️  Không kết nối được MongoDB: {e}")
        logger.warning("🔄 Chạy ở chế độ Mock Data (không cần MongoDB)")
        db = None


async def disconnect_db():
    """Ngắt kết nối MongoDB."""
    global client
    if client:
        client.close()
        logger.info("MongoDB đã ngắt kết nối")


def get_db():
    return db


async def seed_mock_data():
    """Chèn dữ liệu mẫu vào MongoDB nếu chưa có."""
    if db is None:
        return
    from app.utils.mock_data import MOCK_PRODUCTS, MOCK_USERS, MOCK_ORDERS
    
    prod_count = await db.products.count_documents({})
    if prod_count == 0 and MOCK_PRODUCTS:
        await db.products.insert_many([dict(p) for p in MOCK_PRODUCTS])
        logger.info("✅ Đã seed products vào MongoDB")

    user_count = await db.users.count_documents({})
    if user_count == 0 and MOCK_USERS:
        await db.users.insert_many([dict(u) for u in MOCK_USERS])
        logger.info("✅ Đã seed users vào MongoDB")

    order_count = await db.orders.count_documents({})
    if order_count == 0 and MOCK_ORDERS:
        await db.orders.insert_many([dict(o) for o in MOCK_ORDERS])
        logger.info("✅ Đã seed orders vào MongoDB")

