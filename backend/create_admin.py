import asyncio
import os
from datetime import datetime

# Thay đổi thư mục làm việc để import được app
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import connect_db, disconnect_db, get_db
from app.core.security import hash_password
from app.utils.helpers import generate_id

async def create_admin():
    print("Dang ket noi Database...")
    await connect_db()
    db = get_db()
    
    if db is None:
        print("Khong the ket noi MongoDB. Dang chay o che do Mock Data.")
        print("Ban co the dung tai khoan mock mac dinh:")
        print("   Email: admin@agrixanh.vn")
        print("   Mat khau: admin123 hoac password123")
        return

    admin_email = "superadmin@agrixanh.vn"
    admin_password = "superadmin123"
    
    # Kiểm tra xem đã tồn tại chưa
    existing = await db.users.find_one({"email": admin_email})
    if existing:
        print(f"Tai khoan {admin_email} da ton tai!")
        print(f"Mat khau mac dinh la: {admin_password}")
        await disconnect_db()
        return
        
    new_id = f"user_admin_{generate_id()}"
    new_admin = {
        "_id": new_id,
        "email": admin_email,
        "full_name": "Super Admin",
        "phone": "0988888888",
        "address": "He thong AgriXanh",
        "role": "admin",
        "hashed_password": hash_password(admin_password),
        "is_active": True,
        "created_at": datetime.utcnow(),
    }
    
    await db.users.insert_one(new_admin)
    print("Da tao tai khoan admin thanh cong!")
    print(f"Email: {admin_email}")
    print(f"Mat khau: {admin_password}")
    
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(create_admin())
