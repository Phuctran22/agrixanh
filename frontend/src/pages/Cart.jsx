import { useState, useEffect, useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Trash2,
  ShoppingBag,
  ArrowRight,
  Shield,
  Truck,
  MapPin,
  Plus,
  CheckCircle2,
  CreditCard,
  Gift,
  Crown,
  Sparkles,
  HelpCircle,
  X,
  Phone,
  User,
  AlertCircle,
} from 'lucide-react';
import {
  getCart,
  saveCart,
  removeFromCart,
  clearCart,
  getUser,
} from '../store/authStore';
import { ordersAPI, loyaltyAPI } from '../services/api';
import toast from 'react-hot-toast';

const TIER_BADGES = {
  bronze: { label: 'Đồng', emoji: '🥉', color: '#CD7F32', bg: 'bg-amber-100 text-amber-800 border-amber-300' },
  silver: { label: 'Bạc', emoji: '🥈', color: '#9EA5AD', bg: 'bg-slate-100 text-slate-700 border-slate-300' },
  gold: { label: 'Vàng', emoji: '🥇', color: '#F59E0B', bg: 'bg-yellow-100 text-yellow-800 border-yellow-300' },
  diamond: { label: 'Kim Cương', emoji: '💎', color: '#6366F1', bg: 'bg-indigo-100 text-indigo-800 border-indigo-300' },
};

export default function Cart() {
  const navigate = useNavigate();
  const user = getUser();
  const [cart, setCart] = useState(getCart());
  const [submitting, setSubmitting] = useState(false);

  // Address book states
  const [addresses, setAddresses] = useState([]);
  const [selectedAddrId, setSelectedAddrId] = useState('');
  const [showAddAddressModal, setShowAddAddressModal] = useState(false);
  const [newAddr, setNewAddr] = useState({
    recipient_name: user?.full_name || '',
    phone: user?.phone || '',
    address_line: '',
    ward: '',
    district: '',
    province: '',
    is_default: false,
  });

  // Manual fallback address if user has no address in book
  const [manualAddress, setManualAddress] = useState({
    recipient_name: user?.full_name || 'Khách hàng AgriXanh',
    phone: user?.phone || '0901234567',
    address_line: user?.address || '123 Đường Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh',
  });

  // Loyalty states
  const [loyalty, setLoyalty] = useState(null);
  const [usePoints, setUsePoints] = useState(false);
  const [pointsToUse, setPointsToUse] = useState(0);

  // Payment & Note
  const [paymentMethod, setPaymentMethod] = useState('cod');
  const [note, setNote] = useState('');

  // Preview calculation
  const [preview, setPreview] = useState({
    subtotal: 0,
    shipping_fee: 25000,
    discount_amount: 0,
    points_used: 0,
    final_total: 0,
    available_points: 0,
    points_to_earn: 0,
    user_tier: 'bronze',
    is_free_shipping: false,
  });

  // 1. Fetch user address book & loyalty points
  useEffect(() => {
    let isMounted = true;
    const fetchUserData = async () => {
      try {
        const [addrRes, loyRes] = await Promise.allSettled([
          loyaltyAPI.listAddresses(),
          loyaltyAPI.getPoints(),
        ]);

        if (!isMounted) return;

        if (addrRes.status === 'fulfilled' && addrRes.value.data?.items?.length > 0) {
          const list = addrRes.value.data.items;
          setAddresses(list);
          const defaultOne = list.find((a) => a.is_default) || list[0];
          setSelectedAddrId(defaultOne.id || defaultOne._id);
        } else {
          // Default fallback demo address
          const fallbackList = [
            {
              id: 'addr_default_01',
              recipient_name: user?.full_name || 'Khách hàng AgriXanh',
              phone: user?.phone || '0901234567',
              address_line: '123 Đường Nguyễn Huệ',
              ward: 'Phường Bến Nghé',
              district: 'Quận 1',
              province: 'TP. Hồ Chí Minh',
              is_default: true,
            },
          ];
          setAddresses(fallbackList);
          setSelectedAddrId('addr_default_01');
        }

        if (loyRes.status === 'fulfilled') {
          setLoyalty(loyRes.value.data);
        }
      } catch (err) {
        console.warn('Load user addresses/loyalty fallback:', err);
      }
    };

    fetchUserData();
    return () => {
      isMounted = false;
    };
  }, []);

  // 2. Fetch server-side preview calculation whenever cart or points selection changes
  const rawSubtotal = useMemo(
    () => cart.reduce((sum, item) => sum + item.quantity * item.unit_price, 0),
    [cart]
  );

  useEffect(() => {
    if (cart.length === 0) return;

    let isMounted = true;
    const calculatePreview = async () => {
      try {
        const res = await ordersAPI.preview({
          items: cart,
          points_to_use: usePoints ? pointsToUse : 0,
        });
        if (isMounted && res.data) {
          setPreview(res.data);
        }
      } catch (err) {
        // Fallback local calculation
        const isFree = rawSubtotal >= 300000 || loyalty?.tier === 'gold' || loyalty?.tier === 'diamond';
        const ship = isFree ? 0 : 25000;
        const pts = usePoints ? Math.min(pointsToUse, loyalty?.total_points || 0, Math.floor((rawSubtotal * 0.5) / 100)) : 0;
        const discount = pts * 100;
        setPreview({
          subtotal: rawSubtotal,
          shipping_fee: ship,
          discount_amount: discount,
          points_used: pts,
          final_total: Math.max(0, rawSubtotal - discount + ship),
          available_points: loyalty?.total_points || 0,
          points_to_earn: Math.floor((rawSubtotal / 10000) * (loyalty?.tier === 'gold' ? 1.5 : 1.0)),
          user_tier: loyalty?.tier || 'bronze',
          is_free_shipping: isFree,
        });
      }
    };

    calculatePreview();
    return () => {
      isMounted = false;
    };
  }, [cart, rawSubtotal, usePoints, pointsToUse, loyalty]);

  // 3. Cart item helpers
  const updateQuantity = (productId, delta) => {
    const updated = cart
      .map((item) => {
        if (item.product_id === productId) {
          const newQty = item.quantity + delta;
          return newQty > 0 ? { ...item, quantity: newQty } : null;
        }
        return item;
      })
      .filter(Boolean);

    saveCart(updated);
    setCart(updated);
  };

  const handleRemove = (productId) => {
    const updated = removeFromCart(productId);
    setCart(updated);
    toast.success('Đã xóa nông sản khỏi giỏ hàng');
  };

  // 4. Quick Points Helper (Max 50% order value)
  const maxAllowedPoints = useMemo(() => {
    const maxByOrder = Math.floor((rawSubtotal * 0.5) / 100);
    const available = loyalty?.total_points || preview.available_points || 0;
    return Math.max(0, Math.min(available, maxByOrder));
  }, [rawSubtotal, loyalty, preview.available_points]);

  const handleApplyMaxPoints = () => {
    setUsePoints(true);
    setPointsToUse(maxAllowedPoints);
  };

  // 5. Add new address submit
  const handleAddNewAddress = async (e) => {
    e.preventDefault();
    if (!newAddr.recipient_name || !newAddr.phone || !newAddr.address_line) {
      toast.error('Vui lòng điền đầy đủ tên, số điện thoại và địa chỉ');
      return;
    }

    try {
      const res = await loyaltyAPI.addAddress(newAddr);
      const added = res.data;
      setAddresses((prev) => [...prev, added]);
      setSelectedAddrId(added.id || added._id);
      toast.success('Đã thêm địa chỉ giao hàng mới!');
      setShowAddAddressModal(false);
    } catch {
      // Local fallback
      const mockId = `addr_${Date.now()}`;
      const mockItem = { id: mockId, ...newAddr };
      setAddresses((prev) => [...prev, mockItem]);
      setSelectedAddrId(mockId);
      toast.success('Đã lưu địa chỉ nhận hàng');
      setShowAddAddressModal(false);
    }
  };

  // 6. Selected address resolution
  const activeAddress = useMemo(() => {
    if (addresses.length > 0) {
      return addresses.find((a) => (a.id || a._id) === selectedAddrId) || addresses[0];
    }
    return manualAddress;
  }, [addresses, selectedAddrId, manualAddress]);

  // 7. Place Order Submit
  const handleCheckout = async (e) => {
    e.preventDefault();
    if (cart.length === 0) {
      toast.error('Giỏ hàng đang trống');
      return;
    }

    if (!activeAddress || !activeAddress.address_line) {
      toast.error('Vui lòng cung cấp địa chỉ nhận hàng');
      return;
    }

    setSubmitting(true);
    try {
      const formattedAddressString = [
        activeAddress.address_line,
        activeAddress.ward,
        activeAddress.district,
        activeAddress.province,
      ]
        .filter(Boolean)
        .join(', ');

      const orderPayload = {
        customer_id: user?.id || 'user_cust_001',
        customer_name: activeAddress.recipient_name || user?.full_name || 'Khách hàng',
        phone: activeAddress.phone || user?.phone || '0901234567',
        items: cart,
        shipping_address: {
          recipient_name: activeAddress.recipient_name || user?.full_name,
          phone: activeAddress.phone || user?.phone,
          address_line: activeAddress.address_line,
          ward: activeAddress.ward || '',
          district: activeAddress.district || '',
          province: activeAddress.province || '',
          full_text: formattedAddressString,
        },
        payment_method: paymentMethod,
        points_to_use: usePoints ? pointsToUse : 0,
        note: note.trim(),
      };

      const res = await ordersAPI.create(orderPayload);
      clearCart();
      setCart([]);
      const orderCode = res.data?.id ? res.data.id.slice(0, 8).toUpperCase() : 'AGX-2048';
      toast.success(`🎉 Đặt hàng thành công! Mã đơn hàng: #${orderCode}`);
      navigate('/account');
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Không thể tạo đơn hàng, vui lòng thử lại.';
      toast.error(errMsg);
    } finally {
      setSubmitting(false);
    }
  };

  // Empty cart view
  if (cart.length === 0) {
    return (
      <div className="content py-20 text-center">
        <div className="upload-icon mx-auto mb-4 bg-emerald-50 w-16 h-16 rounded-2xl flex items-center justify-center text-[#176b45] shadow-sm">
          <ShoppingBag className="w-8 h-8" />
        </div>
        <h2 className="title mb-2 text-2xl font-black text-[#183229]">Giỏ hàng của bạn đang trống</h2>
        <p className="text-sm text-[#718078] max-w-sm mx-auto mb-6">
          Hãy khám phá các nông sản tươi sạch chuẩn VietGAP đã qua kiểm định AI và bổ sung vào giỏ hàng ngay.
        </p>
        <Link to="/products" className="button primary inline-flex items-center gap-2">
          Khám phá nông sản tươi ngay <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const currentTierBadge = TIER_BADGES[preview.user_tier] || TIER_BADGES.bronze;

  return (
    <div className="content pb-16">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">QUY TRÌNH THANH TOÁN (CHECKOUT)</div>
          <h1 className="title">Hoàn tất Đơn hàng Nông sản</h1>
          <p>Xác nhận giỏ hàng, chọn sổ địa chỉ, áp dụng điểm tích lũy và thanh toán</p>
        </div>
        <div className="draft-badge bg-emerald-100 text-[#176b45] font-bold">
          {cart.length} mặt hàng
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_420px] gap-8 mt-6">
        {/* ========================================================= */}
        {/* CỘT TRÁI: DANH SÁCH GIỎ HÀNG + SỔ ĐỊA CHỈ + THANH TOÁN */}
        {/* ========================================================= */}
        <div className="space-y-6">
          {/* 1. NÔNG SẢN TRONG GIỎ HÀNG */}
          <div className="bg-white rounded-2xl border border-[#dce5df] p-6 shadow-sm">
            <div className="flex items-center justify-between pb-4 border-b border-[#edf1ee] mb-4">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-[#176b45] text-white text-xs font-bold flex items-center justify-center">
                  1
                </span>
                <h2 className="text-base font-extrabold text-[#183229]">Danh mục nông sản đã chọn</h2>
              </div>
              <span className="text-xs text-[#718078]">{cart.length} sản phẩm</span>
            </div>

            <div className="divide-y divide-[#edf1ee]">
              {cart.map((item) => (
                <div key={item.product_id} className="py-4 flex items-center gap-4">
                  <img
                    src={item.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=300'}
                    alt={item.product_name}
                    className="w-16 h-16 rounded-xl object-cover border border-[#dce5df] shrink-0"
                  />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-sm text-[#183229] truncate">{item.product_name}</h3>
                    <div className="flex items-center gap-2 text-xs text-[#718078] mt-0.5">
                      <span>Đơn giá: {Number(item.unit_price).toLocaleString('vi-VN')} đ / {item.unit || 'kg'}</span>
                      {item.seller_id && (
                        <span className="text-[10px] bg-emerald-50 text-emerald-800 px-1.5 py-0.2 rounded font-medium">
                          Nhà vườn: {item.seller_id === 'user_seller_001' ? 'Green Valley Farm' : item.seller_id}
                        </span>
                      )}
                    </div>
                    <div className="inline-flex items-center gap-1 text-[11px] text-[#176b45] font-semibold mt-1">
                      <Shield className="w-3.5 h-3.5" /> Kiểm định AI Đạt chuẩn VietGAP
                    </div>
                  </div>

                  {/* Quantity Stepper */}
                  <div className="flex items-center border border-[#dce5df] rounded-lg bg-[#f9faf8] overflow-hidden shrink-0">
                    <button
                      type="button"
                      className="px-2.5 py-1 text-sm font-bold text-[#718078] hover:bg-[#edf1ee] transition-colors"
                      onClick={() => updateQuantity(item.product_id, -1)}
                    >
                      −
                    </button>
                    <span className="px-3 text-xs font-bold text-[#183229]">{item.quantity}</span>
                    <button
                      type="button"
                      className="px-2.5 py-1 text-sm font-bold text-[#718078] hover:bg-[#edf1ee] transition-colors"
                      onClick={() => updateQuantity(item.product_id, 1)}
                    >
                      +
                    </button>
                  </div>

                  {/* Price & Delete */}
                  <div className="text-right min-w-[100px] shrink-0">
                    <strong className="block text-sm text-[#176b45] font-extrabold font-['Manrope']">
                      {(item.quantity * item.unit_price).toLocaleString('vi-VN')} đ
                    </strong>
                    <button
                      type="button"
                      onClick={() => handleRemove(item.product_id)}
                      className="text-red-400 hover:text-red-600 text-xs mt-1 inline-flex items-center gap-1 transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" /> Xóa
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 2. THIẾT LẬP THÔNG TIN GIAO NHẬN (SỔ ĐỊA CHỈ) */}
          <div className="bg-white rounded-2xl border border-[#dce5df] p-6 shadow-sm">
            <div className="flex items-center justify-between pb-4 border-b border-[#edf1ee] mb-4">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-[#176b45] text-white text-xs font-bold flex items-center justify-center">
                  2
                </span>
                <h2 className="text-base font-extrabold text-[#183229]">Thông tin nhận hàng & Sổ địa chỉ</h2>
              </div>
              <button
                type="button"
                onClick={() => setShowAddAddressModal(true)}
                className="text-xs font-bold text-[#176b45] hover:text-[#125335] inline-flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" /> Thêm địa chỉ mới
              </button>
            </div>

            {/* List addresses from User Book */}
            {addresses.length > 0 ? (
              <div className="space-y-3">
                {addresses.map((addr) => {
                  const aId = addr.id || addr._id;
                  const isSelected = selectedAddrId === aId;
                  return (
                    <label
                      key={aId}
                      className={`flex items-start gap-3 p-4 rounded-xl border cursor-pointer transition-all ${
                        isSelected
                          ? 'border-[#176b45] bg-emerald-50/40 ring-1 ring-[#176b45]'
                          : 'border-[#dce5df] hover:border-[#bdd9c5] bg-white'
                      }`}
                    >
                      <input
                        type="radio"
                        name="shipping_address"
                        className="mt-1 text-[#176b45] focus:ring-[#176b45]"
                        checked={isSelected}
                        onChange={() => setSelectedAddrId(aId)}
                      />
                      <div className="flex-1 text-xs">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-bold text-sm text-[#183229]">{addr.recipient_name}</span>
                          <span className="text-[#718078] flex items-center gap-1 font-medium">
                            <Phone className="w-3 h-3" /> {addr.phone}
                          </span>
                          {addr.is_default && (
                            <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                              Mặc định
                            </span>
                          )}
                        </div>
                        <p className="text-[#516157] leading-relaxed">
                          {[addr.address_line, addr.ward, addr.district, addr.province].filter(Boolean).join(', ')}
                        </p>
                      </div>
                    </label>
                  );
                })}
              </div>
            ) : (
              <div className="space-y-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-[#183229] mb-1">Tên người nhận *</label>
                    <input
                      type="text"
                      className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                      value={manualAddress.recipient_name}
                      onChange={(e) => setManualAddress({ ...manualAddress, recipient_name: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-[#183229] mb-1">Số điện thoại *</label>
                    <input
                      type="tel"
                      className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                      value={manualAddress.phone}
                      onChange={(e) => setManualAddress({ ...manualAddress, phone: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#183229] mb-1">Địa chỉ chi tiết *</label>
                  <textarea
                    rows={2}
                    className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                    value={manualAddress.address_line}
                    onChange={(e) => setManualAddress({ ...manualAddress, address_line: e.target.value })}
                    required
                  />
                </div>
              </div>
            )}
          </div>

          {/* 3. PHƯƠNG THỨC THANH TOÁN */}
          <div className="bg-white rounded-2xl border border-[#dce5df] p-6 shadow-sm">
            <div className="flex items-center gap-2 pb-4 border-b border-[#edf1ee] mb-4">
              <span className="w-6 h-6 rounded-full bg-[#176b45] text-white text-xs font-bold flex items-center justify-center">
                3
              </span>
              <h2 className="text-base font-extrabold text-[#183229]">Phương thức thanh toán</h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {[
                {
                  id: 'cod',
                  title: 'Thanh toán khi nhận hàng (COD)',
                  desc: 'Trả tiền mặt trực tiếp cho shipper khi nhận nông sản',
                  badge: 'Phổ biến',
                },
                {
                  id: 'vnpay',
                  title: 'Cổng thanh toán VNPay',
                  desc: 'Quét mã VNPAY-QR, thẻ ATM nội địa hoặc thẻ Quốc tế',
                  badge: 'Khuyên dùng',
                },
                {
                  id: 'momo',
                  title: 'Ví điện tử MoMo',
                  desc: 'Thanh toán siêu tốc không tiền mặt qua ứng dụng MoMo',
                  badge: 'Nhanh gọn',
                },
                {
                  id: 'zalopay',
                  title: 'Ví ZaloPay',
                  desc: 'Thanh toán tiện lợi tích hợp hệ sinh thái Zalo',
                  badge: 'Tiện lợi',
                },
              ].map((m) => {
                const isSelected = paymentMethod === m.id;
                return (
                  <label
                    key={m.id}
                    className={`flex items-start gap-3 p-4 rounded-xl border cursor-pointer transition-all ${
                      isSelected
                        ? 'border-[#176b45] bg-emerald-50/40 ring-1 ring-[#176b45]'
                        : 'border-[#dce5df] hover:border-[#bdd9c5] bg-white'
                    }`}
                  >
                    <input
                      type="radio"
                      name="payment_method"
                      className="mt-1 text-[#176b45] focus:ring-[#176b45]"
                      checked={isSelected}
                      onChange={() => setPaymentMethod(m.id)}
                    />
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <strong className="text-xs text-[#183229] font-bold">{m.title}</strong>
                        <span className="text-[10px] bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-semibold">
                          {m.badge}
                        </span>
                      </div>
                      <p className="text-[11px] text-[#718078] leading-relaxed">{m.desc}</p>
                    </div>
                  </label>
                );
              })}
            </div>

            {/* Note field */}
            <div className="mt-4 pt-4 border-t border-[#edf1ee]">
              <label className="block text-xs font-bold text-[#183229] mb-1">Ghi chú giao hàng (nếu có)</label>
              <input
                type="text"
                className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df] bg-[#fcfdfc] placeholder:text-[#94a099]"
                placeholder="Ví dụ: Gọi trước khi giao 15 phút, giao giờ hành chính..."
                value={note}
                onChange={(e) => setNote(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* ========================================================= */}
        {/* CỘT PHẢI: ƯU ĐÃI LOYALTY + TỔNG KẾT HÓA ĐƠN ĐẶT HÀNG */}
        {/* ========================================================= */}
        <div className="space-y-6">
          {/* LOYALTY POINTS REDEMPTION CARD */}
          <div className="bg-gradient-to-br from-emerald-900 to-[#123628] rounded-2xl p-5 text-white shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{currentTierBadge.emoji}</span>
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-emerald-200">Hạng thành viên</p>
                  <h3 className="text-sm font-extrabold text-white">{currentTierBadge.label}</h3>
                </div>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-emerald-200">Điểm hiện có</p>
                <p className="text-lg font-black text-amber-300 font-['Manrope']">
                  {Number(loyalty?.total_points || preview.available_points).toLocaleString('vi-VN')} điểm
                </p>
              </div>
            </div>

            <div className="bg-white/10 rounded-xl p-3.5 backdrop-blur-sm border border-white/15">
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 cursor-pointer text-xs font-bold text-white">
                  <input
                    type="checkbox"
                    className="w-4 h-4 rounded text-emerald-500 focus:ring-emerald-400"
                    checked={usePoints}
                    onChange={(e) => {
                      setUsePoints(e.target.checked);
                      if (e.target.checked && pointsToUse === 0) {
                        setPointsToUse(Math.min(maxAllowedPoints, 100));
                      }
                    }}
                  />
                  <span>Dùng điểm tích lũy giảm tiền</span>
                </label>
                <span className="text-[10px] text-emerald-200">1 điểm = 100đ</span>
              </div>

              {usePoints && (
                <div className="mt-3 pt-3 border-t border-white/15">
                  <div className="flex items-center justify-between text-xs mb-1.5">
                    <span className="text-emerald-100">Số điểm sử dụng:</span>
                    <button
                      type="button"
                      onClick={handleApplyMaxPoints}
                      className="text-[10px] font-bold text-amber-300 hover:underline"
                    >
                      Dùng tối đa ({maxAllowedPoints} điểm)
                    </button>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min={0}
                      max={maxAllowedPoints}
                      step={10}
                      className="flex-1 bg-white/20 border border-white/30 text-white rounded-lg px-2.5 py-1.5 text-xs font-bold focus:outline-none focus:ring-2 focus:ring-amber-300"
                      value={pointsToUse}
                      onChange={(e) => setPointsToUse(Math.min(maxAllowedPoints, Math.max(0, Number(e.target.value))))}
                    />
                    <span className="text-xs font-black text-amber-300 shrink-0">
                      - {(pointsToUse * 100).toLocaleString('vi-VN')} đ
                    </span>
                  </div>
                  <p className="text-[10px] text-emerald-200 mt-1.5">
                    * Được dùng tối đa 50% giá trị nông sản trong đơn hàng.
                  </p>
                </div>
              )}
            </div>

            {/* Free shipping perk note */}
            {preview.is_free_shipping ? (
              <div className="flex items-center gap-2 mt-3 text-xs text-emerald-200 bg-emerald-800/40 px-3 py-1.5 rounded-lg border border-emerald-400/20">
                <Truck className="w-4 h-4 text-emerald-300" />
                <span>Bạn được <strong>Miễn phí vận chuyển</strong> theo đặc quyền hạng!</span>
              </div>
            ) : (
              <p className="text-[11px] text-emerald-200/80 mt-2.5">
                Mua thêm {(Math.max(0, 300000 - preview.subtotal)).toLocaleString('vi-VN')}đ để được Free Ship.
              </p>
            )}
          </div>

          {/* ORDER SUMMARY BILL CARD */}
          <div className="bg-white rounded-2xl border border-[#dce5df] p-6 shadow-sm">
            <h3 className="text-base font-extrabold text-[#183229] pb-3 border-b border-[#edf1ee] mb-4">
              Tóm tắt đơn hàng
            </h3>

            <div className="space-y-2.5 text-xs text-[#718078]">
              <div className="flex justify-between">
                <span>Tạm tính nông sản ({cart.length} món)</span>
                <span className="font-semibold text-[#183229]">
                  {preview.subtotal.toLocaleString('vi-VN')} đ
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span>Phí vận chuyển (Giao 2-4h)</span>
                {preview.is_free_shipping ? (
                  <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded text-[11px]">
                    Miễn phí
                  </span>
                ) : (
                  <span className="font-semibold text-[#183229]">
                    {preview.shipping_fee.toLocaleString('vi-VN')} đ
                  </span>
                )}
              </div>

              {preview.discount_amount > 0 && (
                <div className="flex justify-between items-center text-amber-700 font-bold">
                  <span>Giảm giá từ Loyalty Points</span>
                  <span>- {preview.discount_amount.toLocaleString('vi-VN')} đ</span>
                </div>
              )}

              <div className="pt-2 border-t border-[#edf1ee] flex justify-between items-center text-[#176b45] font-semibold text-[11px]">
                <span className="flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5" /> Điểm thưởng dự kiến tích lũy
                </span>
                <span>+ {preview.points_to_earn} điểm</span>
              </div>
            </div>

            {/* FINAL AMOUNT */}
            <div className="pt-4 mt-4 border-t-2 border-[#176b45]/20 flex items-baseline justify-between">
              <div>
                <span className="block text-xs uppercase font-extrabold text-[#718078]">Tổng thanh toán</span>
                <small className="text-[10px] text-[#94a099]">(Đã bao gồm VAT & phí đóng gói)</small>
              </div>
              <strong className="text-2xl font-black text-[#176b45] font-['Manrope']">
                {preview.final_total.toLocaleString('vi-VN')} đ
              </strong>
            </div>

            {/* CHECKOUT BUTTON */}
            <button
              type="button"
              disabled={submitting}
              onClick={handleCheckout}
              className="button primary w-full mt-6 py-3 text-sm font-bold flex items-center justify-center gap-2 shadow-md hover:shadow-lg disabled:opacity-50 transition-all"
            >
              {submitting ? (
                <>Đang khởi tạo đơn hàng...</>
              ) : (
                <>
                  Xác nhận đặt hàng ngay <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

            <div className="mt-4 pt-4 border-t border-[#edf1ee] flex items-center gap-2 text-[11px] text-[#718078]">
              <Shield className="w-4 h-4 text-[#176b45] shrink-0" />
              <span>Cam kết 100% nông sản tươi sạch chuẩn nguồn gốc, đổi trả miễn phí trong 24h.</span>
            </div>
          </div>
        </div>
      </div>

      {/* ========================================================= */}
      {/* MODAL THÊM ĐỊA CHỈ GIAO NHẬN MỚI */}
      {/* ========================================================= */}
      {showAddAddressModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between p-5 border-b border-[#edf1ee] bg-[#f9faf8]">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5 text-[#176b45]" />
                <h3 className="font-extrabold text-[#183229] text-base">Thêm địa chỉ giao nhận mới</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowAddAddressModal(false)}
                className="p-1 rounded-lg hover:bg-slate-200 text-[#718078] transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleAddNewAddress} className="p-5 space-y-3.5">
              <div>
                <label className="block text-xs font-bold text-[#183229] mb-1">Tên người nhận *</label>
                <input
                  type="text"
                  required
                  placeholder="Ví dụ: Nguyễn Văn A"
                  className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df] focus:ring-1 focus:ring-[#176b45]"
                  value={newAddr.recipient_name}
                  onChange={(e) => setNewAddr({ ...newAddr, recipient_name: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#183229] mb-1">Số điện thoại *</label>
                <input
                  type="tel"
                  required
                  placeholder="Ví dụ: 0901234567"
                  className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df] focus:ring-1 focus:ring-[#176b45]"
                  value={newAddr.phone}
                  onChange={(e) => setNewAddr({ ...newAddr, phone: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#183229] mb-1">Địa chỉ chi tiết (Số nhà, tên đường) *</label>
                <input
                  type="text"
                  required
                  placeholder="Ví dụ: 123 Đường Nguyễn Huệ"
                  className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df] focus:ring-1 focus:ring-[#176b45]"
                  value={newAddr.address_line}
                  onChange={(e) => setNewAddr({ ...newAddr, address_line: e.target.value })}
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-bold text-[#183229] mb-1">Phường / Xã</label>
                  <input
                    type="text"
                    placeholder="Phường Bến Nghé"
                    className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                    value={newAddr.ward}
                    onChange={(e) => setNewAddr({ ...newAddr, ward: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#183229] mb-1">Quận / Huyện</label>
                  <input
                    type="text"
                    placeholder="Quận 1"
                    className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                    value={newAddr.district}
                    onChange={(e) => setNewAddr({ ...newAddr, district: e.target.value })}
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#183229] mb-1">Tỉnh / Thành phố</label>
                <input
                  type="text"
                  placeholder="TP. Hồ Chí Minh"
                  className="w-full text-xs p-2.5 rounded-xl border border-[#dce5df]"
                  value={newAddr.province}
                  onChange={(e) => setNewAddr({ ...newAddr, province: e.target.value })}
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-[#edf1ee]">
                <button
                  type="button"
                  onClick={() => setShowAddAddressModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-bold text-[#718078] hover:bg-[#edf1ee]"
                >
                  Hủy bỏ
                </button>
                <button
                  type="submit"
                  className="button primary text-xs py-2 px-4 font-bold"
                >
                  Lưu địa chỉ này
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
