import { useState, useEffect } from 'react';
import {
  Search,
  MoreVertical,
  Eye,
  Package,
  Truck,
  CheckCircle2,
  Clock,
  Printer,
  X,
  Phone,
  MapPin,
  AlertCircle,
  Shield,
  ArrowRight,
} from 'lucide-react';
import { ordersAPI } from '../../services/api';
import { getUser } from '../../store/authStore';
import toast from 'react-hot-toast';

const STATUS_CONFIG = {
  pending:   { label: 'Chờ xác nhận', color: 'bg-amber-100 text-amber-800 border-amber-300' },
  confirmed: { label: 'Đã xác nhận',  color: 'bg-blue-100 text-blue-800 border-blue-300' },
  picking:   { label: 'Đang chuẩn bị', color: 'bg-indigo-100 text-indigo-800 border-indigo-300' },
  shipping:  { label: 'Đang giao hàng', color: 'bg-purple-100 text-purple-800 border-purple-300' },
  delivered: { label: 'Giao thành công', color: 'bg-emerald-100 text-emerald-800 border-emerald-300' },
  cancelled: { label: 'Đã hủy',        color: 'bg-red-100 text-red-700 border-red-300' },
};

export default function SellerOrders() {
  const user = getUser();
  const [orders, setOrders] = useState([]);
  const [statusFilter, setStatusFilter] = useState('All');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const res = await ordersAPI.getAll({
        seller_id: user?.id || 'user_seller_001',
        per_page: 50,
      });
      if (res.data?.items && res.data.items.length > 0) {
        setOrders(res.data.items);
      } else {
        // Sample orders fallback
        setOrders([
          {
            id: 'ord_sample_01',
            customer_name: 'Trần Thị Hoa',
            phone: '0901234567',
            total_amount: 120000,
            subtotal: 95000,
            shipping_fee: 25000,
            discount_amount: 0,
            created_at: new Date().toISOString(),
            order_status: 'pending',
            payment_method: 'cod',
            shipping_address: {
              recipient_name: 'Trần Thị Hoa',
              phone: '0901234567',
              address_line: '123 Đường Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP. HCM',
            },
            items: [
              {
                product_name: 'Cà chua chín mọng Đà Lạt',
                quantity: 2,
                unit_price: 35000,
                unit: 'kg',
                image_url: 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=300',
              },
              {
                product_name: 'Dưa leo baby VietGAP',
                quantity: 1,
                unit_price: 25000,
                unit: 'kg',
                image_url: 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?auto=format&fit=crop&w=300',
              },
            ],
            note: 'Giao giờ hành chính giúp em ạ',
          },
          {
            id: 'ord_sample_02',
            customer_name: 'Bảo Trần',
            phone: '0912345678',
            total_amount: 280000,
            subtotal: 280000,
            shipping_fee: 0,
            discount_amount: 0,
            created_at: new Date(Date.now() - 86400000).toISOString(),
            order_status: 'shipping',
            payment_method: 'momo',
            shipping_address: {
              recipient_name: 'Bảo Trần',
              phone: '0912345678',
              address_line: '456 Lê Duẩn, Quận 1, TP. HCM',
            },
            items: [
              {
                product_name: 'Xoài cát Hòa Lộc Tiền Giang',
                quantity: 3,
                unit_price: 90000,
                unit: 'kg',
                image_url: 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=300',
              },
            ],
            note: '',
          },
          {
            id: 'ord_sample_03',
            customer_name: 'Emma Đào',
            phone: '0987654321',
            total_amount: 680000,
            subtotal: 680000,
            shipping_fee: 0,
            discount_amount: 0,
            created_at: new Date(Date.now() - 172800000).toISOString(),
            order_status: 'delivered',
            payment_method: 'vnpay',
            shipping_address: {
              recipient_name: 'Emma Đào',
              phone: '0987654321',
              address_line: '789 Nam Kỳ Khởi Nghĩa, Quận 3, TP. HCM',
            },
            items: [
              {
                product_name: 'Tỏi cô đơn Lý Sơn chính hiệu',
                quantity: 3,
                unit_price: 220000,
                unit: 'kg',
                image_url: 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?auto=format&fit=crop&w=300',
              },
            ],
            note: 'Đóng thùng xốp cẩn thận',
          },
        ]);
      }
    } catch (err) {
      console.warn('API error, using sample orders:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      await ordersAPI.updateStatus(orderId, newStatus);
      toast.success(`Đã cập nhật trạng thái đơn sang: ${STATUS_CONFIG[newStatus]?.label || newStatus}`);
      setOrders((prev) =>
        prev.map((o) => ((o.id === orderId || o._id === orderId) ? { ...o, order_status: newStatus } : o))
      );
      if (selectedOrder && (selectedOrder.id === orderId || selectedOrder._id === orderId)) {
        setSelectedOrder((prev) => ({ ...prev, order_status: newStatus }));
      }
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Không thể cập nhật trạng thái';
      toast.error(errMsg);
    }
  };

  const getInitials = (name = '') => {
    return name
      .split(' ')
      .filter(Boolean)
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'KH';
  };

  const filtered = orders.filter((o) => {
    const st = o.order_status || 'pending';
    if (statusFilter !== 'All' && st.toLowerCase() !== statusFilter.toLowerCase()) {
      return false;
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      const code = (o.id || o._id || '').toLowerCase();
      const cust = (o.customer_name || '').toLowerCase();
      return code.includes(q) || cust.includes(q);
    }
    return true;
  });

  return (
    <div className="content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">SELLER CENTER / NHÀ VƯỜN</div>
          <h1 className="title">Xử lý & Quản lý Đơn hàng</h1>
          <p>Tiếp nhận đơn phát sinh, đóng gói nông sản và cập nhật tiến trình vận chuyển</p>
        </div>
        <div className="draft-badge bg-emerald-100 text-[#176b45] font-bold">
          {filtered.length} đơn hàng
        </div>
      </div>

      {/* Table Card */}
      <div className="table-card">
        <div className="table-tools">
          <div className="filter-chips">
            {[
              { id: 'All',       label: 'Tất cả đơn' },
              { id: 'pending',   label: 'Chờ xử lý (Pending)' },
              { id: 'picking',   label: 'Đang lấy hàng (Picking)' },
              { id: 'shipping',  label: 'Đang giao (Shipping)' },
              { id: 'delivered', label: 'Hoàn tất (Delivered)' },
              { id: 'cancelled', label: 'Đã hủy (Cancelled)' },
            ].map((f) => (
              <button
                key={f.id}
                className={statusFilter.toLowerCase() === f.id.toLowerCase() ? 'active' : ''}
                onClick={() => setStatusFilter(f.id)}
              >
                {f.label}
              </button>
            ))}
          </div>

          <div className="small-search">
            <Search className="w-4 h-4 text-[#88958e]" />
            <input
              type="text"
              placeholder="Tìm theo mã đơn hoặc tên khách..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-[#718078]">Đang tải danh sách đơn hàng...</div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-[#718078]">Không có đơn hàng nào phù hợp bộ lọc.</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Mã đơn</th>
                <th>Khách hàng</th>
                <th>Sản phẩm cần đóng gói</th>
                <th>Ngày đặt</th>
                <th>Tổng thu</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((o) => {
                const oId = o.id || o._id;
                const displayCode = oId ? oId.replace('ord_', '').slice(0, 8).toUpperCase() : 'AGX-2048';
                const itemsCount = (o.items || []).reduce((sum, it) => sum + (it.quantity || 1), 0);
                const currentStatus = o.order_status || 'pending';
                const cfg = STATUS_CONFIG[currentStatus] || STATUS_CONFIG.pending;

                return (
                  <tr key={oId} className="hover:bg-[#fbfcfb] transition-colors">
                    <td>
                      <strong className="text-[#183229] font-['Manrope'] font-extrabold">
                        #{displayCode}
                      </strong>
                    </td>
                    <td>
                      <div className="customer-cell">
                        <div className="avatar tiny bg-emerald-100 text-emerald-800 font-bold">
                          {getInitials(o.customer_name)}
                        </div>
                        <div>
                          <p className="font-bold text-[#183229] text-xs">{o.customer_name || 'Khách hàng'}</p>
                          <small className="text-[#718078]">{o.phone || ''}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-xs text-[#516157] font-medium">
                        {itemsCount} sản phẩm ({(o.items || []).length} loại)
                      </span>
                    </td>
                    <td>
                      <span className="text-xs text-[#718078]">
                        {new Date(o.created_at || Date.now()).toLocaleDateString('vi-VN', {
                          day: '2-digit', month: '2-digit', year: 'numeric',
                        })}
                      </span>
                    </td>
                    <td>
                      <strong className="text-[#176b45] font-['Manrope'] font-bold text-sm">
                        {Number(o.total_amount || 0).toLocaleString('vi-VN')} đ
                      </strong>
                    </td>
                    <td>
                      <select
                        className={`text-xs font-bold px-2.5 py-1.5 rounded-lg border cursor-pointer focus:outline-none ${cfg.color}`}
                        value={currentStatus}
                        onChange={(e) => handleStatusChange(oId, e.target.value)}
                      >
                        <option value="pending">Chờ xác nhận (Pending)</option>
                        <option value="confirmed">Đã xác nhận (Confirmed)</option>
                        <option value="picking">Đang đóng gói (Picking)</option>
                        <option value="shipping">Đang giao hàng (Shipping)</option>
                        <option value="delivered">Hoàn tất (Delivered)</option>
                        <option value="cancelled">Đã hủy (Cancelled)</option>
                      </select>
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => setSelectedOrder(o)}
                        className="px-2.5 py-1 bg-emerald-50 text-[#176b45] hover:bg-emerald-100 rounded-lg text-xs font-bold inline-flex items-center gap-1 transition-colors"
                        title="Xem chi tiết & Đóng gói"
                      >
                        <Eye className="w-3.5 h-3.5" /> Chi tiết
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* ========================================================= */}
      {/* MODAL CHI TIẾT ĐƠN HÀNG & PHIẾU ĐÓNG GÓI CHO NGƯỜI BÁN */}
      {/* ========================================================= */}
      {selectedOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95">
            {/* Header */}
            <div className="flex items-center justify-between p-5 border-b border-[#edf1ee] bg-[#f9faf8]">
              <div className="flex items-center gap-2">
                <Package className="w-5 h-5 text-[#176b45]" />
                <div>
                  <h3 className="font-extrabold text-[#183229] text-base">
                    Phiếu đóng gói đơn hàng #{selectedOrder.id ? selectedOrder.id.replace('ord_', '').slice(0, 8).toUpperCase() : 'AGX-2048'}
                  </h3>
                  <p className="text-xs text-[#718078]">
                    Ngày đặt: {new Date(selectedOrder.created_at || Date.now()).toLocaleString('vi-VN')}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedOrder(null)}
                className="p-1 rounded-lg hover:bg-slate-200 text-[#718078] transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-5 text-xs">
              {/* Customer & Shipping info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-[#fcfdfc] p-4 rounded-xl border border-[#dce5df]">
                <div>
                  <h4 className="font-bold text-[#183229] uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1">
                    <Phone className="w-3.5 h-3.5 text-[#176b45]" /> Người nhận hàng
                  </h4>
                  <p className="font-extrabold text-sm text-[#183229]">
                    {selectedOrder.shipping_address?.recipient_name || selectedOrder.customer_name}
                  </p>
                  <p className="text-[#516157] mt-0.5">
                    SĐT: {selectedOrder.shipping_address?.phone || selectedOrder.phone}
                  </p>
                </div>
                <div>
                  <h4 className="font-bold text-[#183229] uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-[#176b45]" /> Địa chỉ giao nông sản
                  </h4>
                  <p className="text-[#516157] leading-relaxed">
                    {selectedOrder.shipping_address?.full_text ||
                      (typeof selectedOrder.shipping_address === 'string'
                        ? selectedOrder.shipping_address
                        : [
                            selectedOrder.shipping_address?.address_line,
                            selectedOrder.shipping_address?.ward,
                            selectedOrder.shipping_address?.district,
                            selectedOrder.shipping_address?.province,
                          ].filter(Boolean).join(', '))}
                  </p>
                </div>
              </div>

              {selectedOrder.note && (
                <div className="bg-amber-50 border border-amber-200 p-3 rounded-xl text-amber-900 text-xs flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <strong>Ghi chú từ khách:</strong> {selectedOrder.note}
                  </div>
                </div>
              )}

              {/* Items Table */}
              <div>
                <h4 className="font-extrabold text-sm text-[#183229] mb-3">
                  Danh sách nông sản cần xuất kho & đóng gói
                </h4>
                <div className="border border-[#dce5df] rounded-xl overflow-hidden">
                  <table className="w-full text-xs">
                    <thead className="bg-[#f0f5f2] text-[#516157] font-bold">
                      <tr>
                        <th className="p-3 text-left">Nông sản</th>
                        <th className="p-3 text-center">Số lượng</th>
                        <th className="p-3 text-right">Đơn giá</th>
                        <th className="p-3 text-right">Thành tiền</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#edf1ee]">
                      {(selectedOrder.items || []).map((it, idx) => (
                        <tr key={idx}>
                          <td className="p-3">
                            <div className="flex items-center gap-2.5">
                              <img
                                src={it.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=150'}
                                alt={it.product_name}
                                className="w-9 h-9 rounded-lg object-cover border border-[#dce5df]"
                              />
                              <span className="font-bold text-[#183229]">{it.product_name}</span>
                            </div>
                          </td>
                          <td className="p-3 text-center font-extrabold text-[#183229]">
                            {it.quantity} {it.unit || 'kg'}
                          </td>
                          <td className="p-3 text-right text-[#718078]">
                            {Number(it.unit_price).toLocaleString('vi-VN')} đ
                          </td>
                          <td className="p-3 text-right font-black text-[#176b45]">
                            {(it.quantity * it.unit_price).toLocaleString('vi-VN')} đ
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Total breakdown */}
              <div className="bg-[#f9faf8] p-4 rounded-xl border border-[#edf1ee] space-y-1.5 text-right">
                <div className="flex justify-between text-[#718078]">
                  <span>Tạm tính hàng:</span>
                  <span>{Number(selectedOrder.subtotal || selectedOrder.total_amount).toLocaleString('vi-VN')} đ</span>
                </div>
                <div className="flex justify-between text-[#718078]">
                  <span>Phí vận chuyển:</span>
                  <span>{Number(selectedOrder.shipping_fee || 0).toLocaleString('vi-VN')} đ</span>
                </div>
                {selectedOrder.discount_amount > 0 && (
                  <div className="flex justify-between text-amber-700 font-bold">
                    <span>Giảm giá từ Điểm tích lũy:</span>
                    <span>-{Number(selectedOrder.discount_amount).toLocaleString('vi-VN')} đ</span>
                  </div>
                )}
                <div className="flex justify-between items-baseline pt-2 border-t border-[#dce5df] text-sm">
                  <strong className="text-[#183229]">Tổng giá trị đơn:</strong>
                  <strong className="text-lg font-black text-[#176b45] font-['Manrope']">
                    {Number(selectedOrder.total_amount).toLocaleString('vi-VN')} đ
                  </strong>
                </div>
              </div>

              {/* Workflow status stepper actions */}
              <div className="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200">
                <h4 className="font-extrabold text-xs text-[#183229] mb-2">Chuyển tiếp trạng thái đơn:</h4>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={() => handleStatusChange(selectedOrder.id || selectedOrder._id, 'confirmed')}
                    className="px-3 py-1.5 rounded-lg bg-blue-600 text-white font-bold hover:bg-blue-700 transition-colors"
                  >
                    1. Xác nhận đơn
                  </button>
                  <button
                    type="button"
                    onClick={() => handleStatusChange(selectedOrder.id || selectedOrder._id, 'picking')}
                    className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-bold hover:bg-indigo-700 transition-colors"
                  >
                    2. Đang đóng gói
                  </button>
                  <button
                    type="button"
                    onClick={() => handleStatusChange(selectedOrder.id || selectedOrder._id, 'shipping')}
                    className="px-3 py-1.5 rounded-lg bg-purple-600 text-white font-bold hover:bg-purple-700 transition-colors"
                  >
                    3. Bàn giao shipper
                  </button>
                  <button
                    type="button"
                    onClick={() => handleStatusChange(selectedOrder.id || selectedOrder._id, 'delivered')}
                    className="px-3 py-1.5 rounded-lg bg-emerald-700 text-white font-bold hover:bg-emerald-800 transition-colors"
                  >
                    4. Giao thành công
                  </button>
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-between p-4 border-t border-[#edf1ee] bg-[#f9faf8]">
              <button
                type="button"
                onClick={() => window.print()}
                className="px-3.5 py-2 rounded-xl border border-[#dce5df] bg-white text-[#183229] font-bold inline-flex items-center gap-1.5 hover:bg-slate-50 transition-colors text-xs"
              >
                <Printer className="w-4 h-4" /> In phiếu đóng gói
              </button>
              <button
                type="button"
                onClick={() => setSelectedOrder(null)}
                className="button primary text-xs py-2 px-5 font-bold"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
