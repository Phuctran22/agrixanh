import { useState } from 'react';
import { NavLink, Outlet, useNavigate, Link } from 'react-router-dom';
import {
  Grid,
  Users,
  Sparkles,
  Package,
  Boxes,
  ShoppingCart,
  LogOut,
  Menu,
  Shield,
  Bell,
  ArrowRight,
} from 'lucide-react';
import { getUser, clearAuth } from '../store/authStore';
import toast from 'react-hot-toast';

export default function AdminLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const user = getUser();

  const handleLogout = () => {
    clearAuth();
    toast.success('Đã đăng xuất khỏi Admin Console');
    navigate('/login');
  };

  const navItems = [
    { to: '/admin', label: 'Platform overview', icon: Grid, end: true },
    { to: '/admin/users', label: 'User management', icon: Users },
    { to: '/admin/products', label: 'Products', icon: Package },
    { to: '/admin/categories', label: 'Categories', icon: Boxes },
    { to: '/admin/orders', label: 'Orders', icon: ShoppingCart },
    { to: '/admin/inventory', label: 'Inventory', icon: Boxes },
    { to: '/admin/ai-logs', label: 'AI operations', icon: Sparkles },
  ];

  const getInitials = (name) => {
    if (!name) return 'AD';
    return name
      .split(' ')
      .filter(Boolean)
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  };

  return (
    <div className="app bg-[#f6f8f4] min-h-screen">
      {/* Topbar */}
      <header className="topbar">
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
          <Link to="/" className="button">
            Customer
          </Link>
          <Link to="/seller" className="button">
            Seller Center
          </Link>
          <Link to="/admin" className="button active">
            Admin
          </Link>
        </div>

        {/* Right Actions */}
        <div className="top-actions">
          <button
            className="icon-button mobile-menu"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu className="w-5 h-5" />
          </button>
          <button
            className="icon-button notice"
            onClick={() => toast('Hệ thống hoạt động bình thường', { icon: '🛡️' })}
          >
            <Bell className="w-5 h-5" />
            <i />
          </button>
          <div className="avatar">
            {getInitials(user?.full_name || 'Admin')}
          </div>
          <div className="user-name">
            <strong>{user?.full_name || 'Quản trị viên'}</strong>
            <small>Admin Console</small>
          </div>
          <button
            onClick={handleLogout}
            className="icon-button text-red-500 hover:bg-red-50 ml-1"
            title="Đăng xuất"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Body with Sidebar */}
      <div className="app-body">
        <aside className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
          <div className="sidebar-label">Admin Console</div>
          <nav>
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  onClick={() => setMobileMenuOpen(false)}
                  className={({ isActive }) =>
                    `nav-item ${isActive ? 'selected' : ''}`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Sidebar Mini Card */}
          <div className="sidebar-card">
            <div className="mini-ai">
              <Sparkles className="w-4 h-4 text-[#176b45]" />
            </div>
            <strong>AI Accuracy Index</strong>
            <span>94.8% model precision</span>
            <div className="progress">
              <i style={{ width: '95%' }} />
            </div>
            <Link to="/admin/ai-logs" className="button text-[#176b45] font-bold text-xs">
              View logs <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="sidebar-foot">
            <div className="avatar small">
              {getInitials(user?.full_name || 'Admin')}
            </div>
            <div>
              <strong>{user?.full_name || 'Admin AgriXanh'}</strong>
              <small>System Admin</small>
            </div>
            <button
              onClick={handleLogout}
              className="text-[#98a39d] hover:text-red-500"
              title="Đăng xuất"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </aside>

        {mobileMenuOpen && (
          <div className="scrim" onClick={() => setMobileMenuOpen(false)} />
        )}

        <main className="p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
