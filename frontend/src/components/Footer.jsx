import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-[#dce5df] pt-14 pb-10 mt-16 text-[#5b6961]">
      <div className="content">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="brand mb-3">
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
            <p className="text-xs text-[#718078] leading-relaxed max-w-sm mt-3">
              Nền tảng thương mại điện tử nông sản tích hợp trí tuệ nhân tạo (AI Vision) hỗ trợ phân loại chất lượng minh bạch từ nhà vườn tới bàn ăn.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#183229] mb-4">
              Khám phá
            </h4>
            <ul className="flex flex-col gap-2.5 text-xs">
              <li>
                <Link to="/products" className="text-[#718078] hover:text-[#176b45] transition-colors">
                  Tất cả nông sản
                </Link>
              </li>
              <li>
                <Link to="/ai-check" className="text-[#718078] hover:text-[#176b45] transition-colors">
                  Thử nghiệm phân tích AI
                </Link>
              </li>
              <li>
                <Link to="/seller" className="text-[#718078] hover:text-[#176b45] transition-colors">
                  Dành cho nhà vườn (Seller)
                </Link>
              </li>
              <li>
                <Link to="/admin" className="text-[#718078] hover:text-[#176b45] transition-colors">
                  Quản trị hệ thống (Admin)
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#183229] mb-4">
              Hỗ trợ & Bảo đảm
            </h4>
            <ul className="flex flex-col gap-2.5 text-xs">
              <li>
                <span className="text-[#718078]">Độ tươi chuẩn AI: 98% cam kết</span>
              </li>
              <li>
                <span className="text-[#718078]">Truy xuất nguồn gốc nhà vườn</span>
              </li>
              <li>
                <span className="text-[#718078]">Giao nhanh trong 2-4 giờ</span>
              </li>
              <li>
                <span className="text-[#718078]">Hỗ trợ: support@agrixanh.vn</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-[#edf1ee] flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-[#9aa49f]">
          <p>© {new Date().getFullYear()} AgriXanh Inc. Phát triển theo chuẩn giao diện AgriXanh UI Design.</p>
          <div className="flex gap-4">
            <span>FastAPI Backend</span>
            <span>•</span>
            <span>React + Tailwind</span>
            <span>•</span>
            <span>Gemini AI Vision</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
