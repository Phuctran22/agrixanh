import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { setAuth } from '../store/authStore';
import toast from 'react-hot-toast';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await authAPI.login({ email, password });
      setAuth(res.data.access_token, res.data.user);
      toast.success('Đăng nhập thành công!');
      if (res.data.user.role === 'admin') navigate('/admin');
      else if (res.data.user.role === 'seller') navigate('/seller');
      else navigate('/');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Đăng nhập thất bại');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (emailVal, passVal) => {
    setEmail(emailVal);
    setPassword(passVal);
    setLoading(true);
    try {
      const res = await authAPI.login({ email: emailVal, password: passVal });
      setAuth(res.data.access_token, res.data.user);
      toast.success(`Đăng nhập thành công: ${res.data.user.full_name}`);
      if (res.data.user.role === 'admin') navigate('/admin');
      else if (res.data.user.role === 'seller') navigate('/seller');
      else navigate('/');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Đăng nhập thất bại');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="content flex items-center justify-center py-12">
      <div className="form-card max-w-md w-full shadow-xl">
        <div className="text-center mb-6">
          <div className="logo mx-auto mb-3">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 4c-8 0-14 4-14 10 0 3 2 5 5 5 6 0 9-7 9-15Z" />
              <path d="M4 21c2-6 6-10 12-13" />
            </svg>
          </div>
          <h2 className="title text-2xl">Đăng nhập tài khoản</h2>
          <p className="text-xs text-[#718078] mt-1">Hệ sinh thái thương mại nông sản thông minh AgriXanh</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="field">
            <span>Địa chỉ Email</span>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="ten@agrixanh.vn"
            />
          </div>

          <div className="field">
            <span>Mật khẩu</span>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="button primary w-full mt-2"
          >
            {loading ? 'Đang xử lý...' : 'Đăng nhập ngay'}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-[#718078]">
          Chưa có tài khoản?{' '}
          <Link to="/register" className="font-bold text-[#176b45] hover:underline">
            Đăng ký tài khoản mới
          </Link>
        </div>

        {/* Quick test logins */}
        <div className="mt-6 pt-5 border-t border-[#edf1ee] text-xs">
          <p className="font-bold text-[#53645b] mb-2 text-center">Đăng nhập nhanh 1-Click thử nghiệm:</p>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() => handleQuickLogin('customer@agrixanh.vn', 'customer123')}
              className="px-2 py-1.5 bg-[#edf7f1] text-[#176b45] font-semibold text-[11px] rounded-lg border border-[#bad9c5] hover:bg-[#dff4e8] transition-colors"
            >
              👤 Khách mua
            </button>
            <button
              type="button"
              onClick={() => handleQuickLogin('seller@agrixanh.vn', 'seller123')}
              className="px-2 py-1.5 bg-[#edf7f1] text-[#176b45] font-semibold text-[11px] rounded-lg border border-[#bad9c5] hover:bg-[#dff4e8] transition-colors"
            >
              🌱 Người bán
            </button>
            <button
              type="button"
              onClick={() => handleQuickLogin('admin@agrixanh.vn', 'admin123')}
              className="px-2 py-1.5 bg-[#edf7f1] text-[#176b45] font-semibold text-[11px] rounded-lg border border-[#bad9c5] hover:bg-[#dff4e8] transition-colors"
            >
              🛡️ Quản trị
            </button>
          </div>
          <p className="text-[10px] text-center text-[#718078] mt-2">
            Mật khẩu demo: <span className="font-mono">customer123</span> / <span className="font-mono">seller123</span> / <span className="font-mono">admin123</span>
          </p>
        </div>
      </div>
    </div>
  );
}
