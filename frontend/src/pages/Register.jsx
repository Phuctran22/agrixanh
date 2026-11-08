import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    role: 'customer',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authAPI.register(formData);
      toast.success('Đăng ký thành công! Vui lòng đăng nhập.');
      navigate('/login');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Đăng ký thất bại. Vui lòng thử lại.');
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
          <h2 className="title text-2xl">Đăng ký thành viên</h2>
          <p className="text-xs text-[#718078] mt-1">Đồng hành cùng nền nông nghiệp xanh bền vững</p>
        </div>

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="field">
            <span>Họ và tên</span>
            <input
              type="text"
              name="full_name"
              required
              value={formData.full_name}
              onChange={handleChange}
              placeholder="Nguyễn Văn An"
            />
          </div>

          <div className="field">
            <span>Địa chỉ Email</span>
            <input
              type="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              placeholder="an@example.com"
            />
          </div>

          <div className="field">
            <span>Số điện thoại</span>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="0912345678"
            />
          </div>

          <div className="field">
            <span>Mật khẩu</span>
            <input
              type="password"
              name="password"
              required
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
            />
          </div>

          <div className="field">
            <span>Loại tài khoản tham gia</span>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="customer">Người mua nông sản (Customer)</option>
              <option value="seller">Chủ nhà vườn / Đối tác bán (Seller)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="button primary w-full mt-2"
          >
            {loading ? 'Đang tạo tài khoản...' : 'Tạo tài khoản ngay'}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-[#718078]">
          Đã có tài khoản?{' '}
          <Link to="/login" className="font-bold text-[#176b45] hover:underline">
            Đăng nhập ngay
          </Link>
        </div>
      </div>
    </div>
  );
}
