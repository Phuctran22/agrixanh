# 🌿 AgriXanh - Hệ thống Thương mại Điện tử Nông sản Tích hợp AI

AgriXanh là nền tảng thương mại điện tử chuyên biệt cho nông sản sạch, tích hợp trí tuệ nhân tạo (AI Vision) hỗ trợ nhận diện chất lượng, quản lý đơn hàng, kho vận và chăm sóc khách hàng.

## 🚀 Cấu trúc dự án

```
AgriXanh/
├── backend/            # FastAPI backend (Python)
│   ├── app/            # API routers, models, core configs
│   ├── main.py         # Entry point FastAPI
│   └── requirements.txt
├── frontend/           # React + Vite frontend
│   ├── src/            # Components, pages, layouts, store
│   └── package.json
├── diagrams/           # Sơ đồ thiết kế hệ thống
└── run_backend.bat     # Script chạy nhanh backend
└── run_frontend.bat    # Script chạy nhanh frontend
```

## 🛠️ Hướng dẫn cài đặt & Chạy

### 1. Backend (FastAPI + MongoDB)
```bash
cd backend
python -m venv venv
# Kích hoạt venv (Windows):
.\venv\Scripts\activate
# Cài đặt thư viện:
pip install -r requirements.txt
# Cấu hình biến môi trường:
cp .env.example .env
# Chạy server:
uvicorn main:app --reload
```
API Documentation: `http://localhost:8000/docs`

### 2. Frontend (React + Vite)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Giao diện người dùng: `http://localhost:5173`
