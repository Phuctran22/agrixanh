import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  TrendingUp,
  Package,
  ShoppingCart,
  Sparkles,
  Plus,
  ArrowRight,
  Boxes,
} from 'lucide-react';
import { statsAPI } from '../../services/api';
import { getUser } from '../../store/authStore';

export default function SellerDashboard() {
  const user = getUser();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    statsAPI
      .getSellerStats(user?.id || 'user_seller_001')
      .then((res) => setStats(res.data))
      .catch((err) => console.warn('Using fallback seller stats:', err));
  }, [user]);

  const bars = [35, 48, 42, 66, 52, 76, 88, 70, 92, 74, 82, 96];
  const months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'];

  const alertItems = [
    {
      name: 'Cà chua chín mọng Đà Lạt',
      remaining: '4 kg còn lại',
      image: 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=300',
    },
    {
      name: 'Cà rốt giòn ngọt Mộc Châu',
      remaining: '8 kg còn lại',
      image: 'https://images.unsplash.com/photo-1609842947419-ba4f04d5d60f?auto=format&fit=crop&w=300',
    },
    {
      name: 'Hộp rau xanh thu hoạch',
      remaining: '12 hộp còn lại',
      image: 'https://images.unsplash.com/photo-1723347101054-c246b0034f11?auto=format&fit=crop&w=300',
    },
  ];

  return (
    <div className="content seller-content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">SELLER CENTER</div>
          <h1 className="title">Chào buổi sáng, {user?.full_name || 'An Minh'}</h1>
          <p>Tình hình hoạt động gian hàng nông sản của bạn hôm nay.</p>
        </div>
        <Link to="/seller/ai-evaluate" className="button primary">
          <Plus className="w-4 h-4" /> Đăng nông sản mới
        </Link>
      </div>

      {/* 4 Stat Cards from Figma */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Doanh số bán</span>
          <strong>{stats?.total_revenue ? Number(stats.total_revenue).toLocaleString('vi-VN') + ' đ' : '128.400.000 đ'}</strong>
          <small>+18.2% so với tháng trước</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <ShoppingCart className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Tổng đơn hàng</span>
          <strong>{stats?.total_orders || '368'}</strong>
          <small>+8.4% tỷ lệ giao thành công</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Boxes className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Nông sản niêm yết</span>
          <strong>{stats?.total_products || '42'}</strong>
          <small className="text-[#ef8b45]">3 mặt hàng sắp hết</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Sparkles className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Lượt kiểm định AI</span>
          <strong>1,248</strong>
          <small>98.2% độ tin cậy chuẩn</small>
        </div>
      </div>

      {/* Dashboard Grid: Chart + Inventory Alerts */}
      <div className="dashboard-grid">
        {/* Sales Performance Chart */}
        <div className="chart-card">
          <div className="card-top">
            <div>
              <strong>Biểu đồ tăng trưởng doanh số</strong>
              <small>Thống kê 12 tháng gần nhất</small>
            </div>
            <strong>
              84.200.000 đ <span>+12.5%</span>
            </strong>
          </div>

          <div className="chart">
            <div className="y-labels">
              <span>80tr</span>
              <span>60tr</span>
              <span>40tr</span>
              <span>20tr</span>
              <span>0</span>
            </div>
            <div className="bars">
              {bars.map((h, i) => (
                <div key={i} className={i === 11 ? 'hot' : ''}>
                  <i style={{ height: `${h}%` }} />
                  <span>{months[i]}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Inventory Alerts Card */}
        <div className="alerts-card">
          <div className="card-top">
            <div>
              <strong>Cảnh báo kho hàng</strong>
              <small>Nông sản cần bổ sung thu hoạch</small>
            </div>
            <span className="alert-count">3</span>
          </div>

          <div className="mt-4">
            {alertItems.map((item) => (
              <div className="alert-item" key={item.name}>
                <img src={item.image} alt={item.name} />
                <div>
                  <strong>{item.name}</strong>
                  <small>{item.remaining}</small>
                </div>
                <Link to="/seller/inventory" className="button">
                  <ArrowRight className="w-4 h-4 text-[#8b9891]" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
