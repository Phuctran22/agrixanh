import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Layouts
import UserLayout from './layouts/UserLayout';
import SellerLayout from './layouts/SellerLayout';
import AdminLayout from './layouts/AdminLayout';

// 1. Phân hệ Khách hàng (Customer Pages)
import Home from './pages/Home';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import AICheck from './pages/AICheck';
import Cart from './pages/Cart';
import Profile from './pages/Profile';
import AccountPage from './pages/AccountPage';
import Login from './pages/Login';
import Register from './pages/Register';

// 2. Phân hệ Người bán (Seller Pages)
import SellerDashboard from './pages/seller/SellerDashboard';
import SellerProducts from './pages/seller/SellerProducts';
import SellerAIEvaluate from './pages/seller/SellerAIEvaluate';
import SellerOrders from './pages/seller/SellerOrders';
import SellerInventory from './pages/seller/SellerInventory';

// 3. Phân hệ Quản trị viên (Admin Pages)
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminProducts from './pages/admin/AdminProducts';
import AdminCategories from './pages/admin/AdminCategories';
import AdminOrders from './pages/admin/AdminOrders';
import AdminInventory from './pages/admin/AdminInventory';
import AdminUsers from './pages/admin/AdminUsers';
import AdminAILogs from './pages/admin/AdminAILogs';

import { getUser } from './store/authStore';

// Protected Route Guard with Role Verification
const ProtectedRoute = ({ children, adminOnly = false, allowedRoles = null }) => {
  const user = getUser();
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (adminOnly && user.role !== 'admin') {
    return <Navigate to="/" replace />;
  }
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#0a1d13',
            color: '#fff',
            border: '1px solid #166534',
            fontSize: '13px',
            borderRadius: '12px',
          },
        }}
      />

      <Routes>
        {/* ============================================================ */}
        {/* 1. PHÂN HỆ KHÁCH HÀNG (Customer Portal)                     */}
        {/* ============================================================ */}
        <Route element={<UserLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/ai-check" element={<AICheck />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/account"
            element={
              <ProtectedRoute>
                <AccountPage />
              </ProtectedRoute>
            }
          />
        </Route>

        {/* ============================================================ */}
        {/* 2. PHÂN HỆ NGƯỜI BÁN (Seller Center / Nhà Vườn)             */}
        {/* ============================================================ */}
        <Route
          path="/seller"
          element={
            <ProtectedRoute allowedRoles={['seller', 'admin']}>
              <SellerLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<SellerDashboard />} />
          <Route path="products" element={<SellerProducts />} />
          <Route path="ai-evaluate" element={<SellerAIEvaluate />} />
          <Route path="orders" element={<SellerOrders />} />
          <Route path="inventory" element={<SellerInventory />} />
        </Route>

        {/* ============================================================ */}
        {/* 3. PHÂN HỆ QUẢN TRỊ VIÊN (Admin Central Portal)             */}
        {/* ============================================================ */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly>
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminDashboard />} />
          <Route path="products" element={<AdminProducts />} />
          <Route path="categories" element={<AdminCategories />} />
          <Route path="orders" element={<AdminOrders />} />
          <Route path="inventory" element={<AdminInventory />} />
          <Route path="users" element={<AdminUsers />} />
          <Route path="ai-logs" element={<AdminAILogs />} />
        </Route>

        {/* 404 Route */}
        <Route
          path="*"
          element={
            <div className="min-h-screen bg-[#050f0a] flex flex-col items-center justify-center text-center px-4">
              <h1 className="text-6xl font-black text-lime-400 mb-2">404</h1>
              <p className="text-xl text-white font-bold mb-4">Trang không tồn tại</p>
              <a
                href="/"
                className="px-6 py-2.5 bg-green-600 hover:bg-green-500 text-white rounded-xl text-sm font-semibold transition-colors"
              >
                Về trang chủ AgriXanh
              </a>
            </div>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
