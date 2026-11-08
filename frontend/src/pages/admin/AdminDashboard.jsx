import { useState, useEffect } from 'react';
import {
  Users,
  Shield,
  TrendingUp,
  Sparkles,
  ArrowRight,
  Package,
  ShoppingCart,
} from 'lucide-react';
import { statsAPI } from '../../services/api';

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    statsAPI
      .getDashboard()
      .then((res) => setData(res.data))
      .catch((err) => console.warn('Using fallback admin stats:', err));
  }, []);

  return (
    <div className="content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">ADMIN CONSOLE</div>
          <h1 className="title">Platform Overview</h1>
          <p>Báo cáo hiệu suất toàn bộ hệ sinh thái sàn thương mại AgriXanh.</p>
        </div>
        <div className="date-pill">
          01 Tháng 10 – 31 Tháng 10, 2026
        </div>
      </div>

      {/* 4 Stat Cards */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Users className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Tổng người dùng</span>
          <strong>{data?.total_users ? data.total_users.toLocaleString('vi-VN') : '24,892'}</strong>
          <small>+12.8% thành viên mới</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Shield className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Nhà vườn đối tác</span>
          <strong>1,248</strong>
          <small>+48 hợp tác xã tháng này</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Tổng doanh thu sàn</span>
          <strong>{data?.total_revenue ? Number(data.total_revenue).toLocaleString('vi-VN') + ' đ' : '284.600.000 đ'}</strong>
          <small>+18.2% tăng trưởng</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Sparkles className="w-5 h-5 text-[#176b45]" />
          </div>
          <span>Lượt kiểm định AI</span>
          <strong>86,420</strong>
          <small>98.1% độ tin cậy</small>
        </div>
      </div>

      {/* Admin Hero Banner with Orbit Animation Graphic */}
      <div className="admin-hero">
        <div>
          <div className="eyebrow">AI QUALITY NETWORK</div>
          <div className="admin-title">
            86,420 lượt kiểm định kiến tạo<br />
            hệ thống nông sản minh bạch.
          </div>
          <p>
            Mỗi lượt quét AI hỗ trợ nâng cao tính minh bạch, trao quyền cho nhà vườn và xây dựng niềm tin trọn vẹn cho người tiêu dùng.
          </p>

          <div className="admin-metrics">
            <div>
              <strong>94.8%</strong>
              <span>Độ chuẩn xác phân hạng</span>
            </div>
            <div>
              <strong>1.8s</strong>
              <span>Tốc độ phản hồi AI</span>
            </div>
            <div>
              <strong>99.2%</strong>
              <span>Thời gian hoạt động</span>
            </div>
          </div>
        </div>

        {/* Interactive Orbit Graphic from Figma */}
        <div className="orbit">
          <div className="orbit-core">
            <Sparkles className="w-8 h-8 mx-auto mb-1 text-emerald-300" />
            <span>AI</span>
          </div>
          <i className="orbit-one" />
          <i className="orbit-two" />
          <b className="dot d1" />
          <b className="dot d2" />
          <b className="dot d3" />
        </div>
      </div>
    </div>
  );
}
