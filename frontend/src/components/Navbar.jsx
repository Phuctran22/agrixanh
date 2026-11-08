import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { ShoppingBag, Bell, Menu, X, LogOut, Sparkles, Shield, User, ArrowRight, Crown } from 'lucide-react';
import { getUser, clearAuth, getCart } from '../store/authStore';
import toast from 'react-hot-toast';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0);
  const location = useLocation();
  const navigate = useNavigate();
  const user = getUser();

  const isCustomer = !location.pathname.startsWith('/seller') && !location.pathname.startsWith('/admin');
  const isSeller = location.pathname.startsWith('/seller');
  const isAdmin = location.pathname.startsWith('/admin');

  useEffect(() => {
    const updateCart = () => setCartCount(getCart().length);
    updateCart();
    const interval = setInterval(updateCart, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    clearAuth();
    toast.success('Đã đăng xuất tài khoản');
    navigate('/login');
  };

  const getInitials = (name) => {
    if (!name) return 'AM';
    return name
      .split(' ')
      .filter(Boolean)
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  };

  return (
    <header className="topbar">
      {/* Brand */}
      <Link to="/" className="brand">
        <div className="logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 4c-8 0-14 4-14 10 0 3 2 5 5 5 6 0 9-7 9-15Z" />
            <path d="M4 21c2-6 6-10 12-13" />
          </svg>
        </div>
        <div>
          <strong>AgriXanh</strong>
          <small>Grow green. Live well.</small>
        </div>
      </Link>

      {/* Central Portal Switch */}
      <div className="portal-switch hidden sm:flex">
        <Link
          to="/"
          className={`button ${isCustomer ? 'active' : ''}`}
        >
          Khách hàng
        </Link>
        <Link
          to="/seller"
          className={`button ${isSeller ? 'active' : ''}`}
        >
          Kênh Người bán
        </Link>
        <Link
          to="/admin"
          className={`button ${isAdmin ? 'active' : ''}`}
        >
          Quản trị Admin
        </Link>
      </div>

      {/* Top Actions */}
      <div className="top-actions">
        {/* Navigation shortcut links */}
        <div className="hidden lg:flex items-center gap-4 mr-2">
          <Link
            to="/products"
            className="text-xs font-semibold text-[#53655d] hover:text-[#176b45] transition-colors"
          >
            Nông sản
          </Link>
          <Link
            to="/ai-check"
            className="text-xs font-semibold text-[#176b45] hover:text-[#115a39] flex items-center gap-1.5 bg-[#edf7f1] px-2.5 py-1 rounded-lg"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#176b45]" />
            <span>AI Check</span>
          </Link>
        </div>

        {/* Cart */}
        <Link
          to="/cart"
          className="icon-button relative"
          title="Giỏ hàng nông sản"
        >
          <ShoppingBag className="w-5 h-5" />
          {cartCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-[#ef8b45] text-white text-[10px] font-bold rounded-full flex items-center justify-center shadow-sm">
              {cartCount}
            </span>
          )}
        </Link>

        {/* Notifications */}
        <button
          type="button"
          className="icon-button notice"
          title="Thông báo hệ thống"
          onClick={() => toast('Không có thông báo mới', { icon: '🔔' })}
        >
          <Bell className="w-5 h-5" />
          <i />
        </button>

        {/* User profile / Auth */}
        {user ? (
          <div className="flex items-center gap-2">
            <Link to="/account" className="flex items-center gap-2 group" title="Tài khoản & Loyalty">
              {user?.avatar_url ? (
                <img src={user.avatar_url} alt="" className="w-9 h-9 rounded-xl object-cover border border-[#dce5df]" />
              ) : (
                <div className="avatar">{getInitials(user.full_name)}</div>
              )}
              <div className="user-name text-left hidden md:block">
                <strong className="group-hover:text-[#176b45] transition-colors">{user.full_name || 'Khách hàng'}</strong>
                <small>
                  {user.role === 'admin'
                    ? 'Quản trị viên'
                    : user.role === 'seller'
                    ? 'Nhà vườn đối tác'
                    : '✦ Thành viên'}
                </small>
              </div>
            </Link>
            <button
              onClick={handleLogout}
              className="icon-button text-red-500 hover:bg-red-50"
              title="Đăng xuất"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Link
              to="/login"
              className="text-xs font-bold text-[#176b45] hover:bg-[#edf7f1] px-3 py-1.5 rounded-lg transition-colors"
            >
              Đăng nhập
            </Link>
            <Link
              to="/register"
              className="text-xs font-bold text-white bg-[#176b45] hover:bg-[#115a39] px-3.5 py-1.5 rounded-lg shadow-sm transition-colors"
            >
              Đăng ký
            </Link>
          </div>
        )}

        {/* Mobile menu trigger */}
        <button
          className="icon-button mobile-menu"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle mobile menu"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="fixed top-[76px] left-0 right-0 bg-white border-b border-[#dce5df] p-4 shadow-xl z-50 flex flex-col gap-3">
          <div className="text-xs font-bold uppercase text-[#94a099] tracking-wider mb-1">
            Chuyển phân hệ
          </div>
          <div className="grid grid-cols-3 gap-2">
            <Link
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              className={`text-center py-2 text-xs font-bold rounded-lg border ${
                isCustomer ? 'bg-[#176b45] text-white border-[#176b45]' : 'bg-[#f6f8f4] text-[#66766e] border-[#dce5df]'
              }`}
            >
              Khách hàng
            </Link>
            <Link
              to="/seller"
              onClick={() => setMobileMenuOpen(false)}
              className={`text-center py-2 text-xs font-bold rounded-lg border ${
                isSeller ? 'bg-[#176b45] text-white border-[#176b45]' : 'bg-[#f6f8f4] text-[#66766e] border-[#dce5df]'
              }`}
            >
              Người bán
            </Link>
            <Link
              to="/admin"
              onClick={() => setMobileMenuOpen(false)}
              className={`text-center py-2 text-xs font-bold rounded-lg border ${
                isAdmin ? 'bg-[#176b45] text-white border-[#176b45]' : 'bg-[#f6f8f4] text-[#66766e] border-[#dce5df]'
              }`}
            >
              Admin
            </Link>
          </div>

          <div className="h-px bg-[#dce5df] my-2" />

          <Link
            to="/products"
            onClick={() => setMobileMenuOpen(false)}
            className="py-2 text-sm font-semibold text-[#183229] hover:text-[#176b45]"
          >
            Khám phá Nông sản
          </Link>
          <Link
            to="/ai-check"
            onClick={() => setMobileMenuOpen(false)}
            className="py-2 text-sm font-semibold text-[#176b45] flex items-center justify-between"
          >
            <span>Trực tiếp Kiểm định AI</span>
            <Sparkles className="w-4 h-4" />
          </Link>
          <Link
            to="/cart"
            onClick={() => setMobileMenuOpen(false)}
            className="py-2 text-sm font-semibold text-[#183229] flex items-center justify-between"
          >
            <span>Giỏ hàng</span>
            <span className="bg-[#ef8b45] text-white text-xs font-bold px-2 py-0.5 rounded-full">{cartCount}</span>
          </Link>

          {user && (
            <>
              <Link
                to="/account"
                onClick={() => setMobileMenuOpen(false)}
                className="py-2 text-sm font-semibold text-[#183229] flex items-center gap-2"
              >
                <Crown className="w-4 h-4 text-[#176b45]" /> Tài khoản & Thành viên
              </Link>
              <Link
                to="/profile"
                onClick={() => setMobileMenuOpen(false)}
                className="py-2 text-sm font-semibold text-[#183229]"
              >
                Hồ sơ & Đơn hàng của tôi
              </Link>
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleLogout();
                }}
                className="text-left py-2 text-sm font-bold text-red-600"
              >
                Đăng xuất ({user.full_name})
              </button>
            </>
          )}
        </div>
      )}
    </header>
  );
}
