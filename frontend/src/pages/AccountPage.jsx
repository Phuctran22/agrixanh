import { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import {
  User, MapPin, Crown, LogOut, Plus, Trash2, Edit2, Star,
  Check, ChevronRight, Phone, Home, Sparkles, Gift, Shield,
  TrendingUp, Package, Calendar, X, Save, Camera, Truck, Clock,
  ShoppingBag, CheckCircle2, RotateCcw, AlertTriangle, ArrowRight,
} from 'lucide-react';
import { getUser, setAuth, clearAuth, addToCart } from '../store/authStore';
import { loyaltyAPI, ordersAPI } from '../services/api';
import toast from 'react-hot-toast';

/* ─────────────────────────── TIER CONFIG (mirror backend) ─────────────────── */
const TIER_CONFIG = {
  bronze:  { label: 'Đồng',      emoji: '🥉', color: '#CD7F32', bg: 'from-amber-700/20 to-amber-600/10', border: 'border-amber-400/30', badge: 'bg-amber-100 text-amber-800' },
  silver:  { label: 'Bạc',       emoji: '🥈', color: '#9EA5AD', bg: 'from-slate-400/20 to-slate-300/10', border: 'border-slate-400/30', badge: 'bg-slate-100 text-slate-700' },
  gold:    { label: 'Vàng',      emoji: '🥇', color: '#F59E0B', bg: 'from-yellow-400/20 to-amber-300/10', border: 'border-yellow-400/30', badge: 'bg-yellow-100 text-yellow-800' },
  diamond: { label: 'Kim Cương', emoji: '💎', color: '#6366F1', bg: 'from-indigo-400/20 to-purple-400/10', border: 'border-indigo-400/30', badge: 'bg-indigo-100 text-indigo-800' },
};

const TIER_THRESHOLDS = { bronze: 0, silver: 2_000_000, gold: 5_000_000, diamond: 15_000_000 };
const TIER_ORDER = ['bronze', 'silver', 'gold', 'diamond'];

const fmt = (n) => Number(n || 0).toLocaleString('vi-VN') + 'đ';
const fmtPts = (n) => Number(n || 0).toLocaleString('vi-VN') + ' điểm';

/* ─────────────────────────── AVATAR INITIALS ───────────────────────────────── */
function AvatarEl({ user, size = 'lg', onClick }) {
  const initials = (user?.full_name || user?.email || 'U')
    .split(' ').filter(Boolean).map((w) => w[0]).slice(0, 2).join('').toUpperCase();
  const sizeMap = { lg: 'w-20 h-20 text-2xl', md: 'w-12 h-12 text-base', sm: 'w-8 h-8 text-xs' };
  return user?.avatar_url ? (
    <img
      src={user.avatar_url}
      alt={user.full_name}
      onClick={onClick}
      className={`${sizeMap[size]} rounded-2xl object-cover border-2 border-white shadow-lg cursor-pointer`}
    />
  ) : (
    <div
      onClick={onClick}
      className={`${sizeMap[size]} rounded-2xl grid place-items: center font-bold cursor-pointer
        bg-gradient-to-br from-emerald-500 to-teal-600 text-white shadow-lg`}
      style={{ display: 'grid', placeItems: 'center' }}
    >
      {initials}
    </div>
  );
}

/* ─────────────────────────── TIER PROGRESS BAR ─────────────────────────────── */
function TierProgressBar({ loyalty }) {
  if (!loyalty) return null;
  const tier = loyalty.tier || 'bronze';
  const cfg  = TIER_CONFIG[tier] || TIER_CONFIG.bronze;
  const idx  = TIER_ORDER.indexOf(tier);
  const pct  = loyalty.progress_pct ?? 0;
  const nextTierLabel = idx < TIER_ORDER.length - 1
    ? TIER_CONFIG[TIER_ORDER[idx + 1]].label : null;

  return (
    <div className={`rounded-2xl border p-5 bg-gradient-to-br ${cfg.bg} ${cfg.border}`}>
      {/* Tier badge */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{cfg.emoji}</span>
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-[#718078]">Hạng thành viên</p>
            <h3 className="text-lg font-extrabold" style={{ color: cfg.color }}>{cfg.label}</h3>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-[#718078]">Điểm hiện có</p>
          <p className="text-xl font-black text-[#183229]">{fmtPts(loyalty.total_points)}</p>
        </div>
      </div>

      {/* Progress bar */}
      {tier !== 'diamond' && (
        <>
          <div className="flex justify-between text-xs text-[#718078] mb-1.5">
            <span>{cfg.label}</span>
            <span className="font-semibold">{pct.toFixed(0)}%</span>
            <span>{nextTierLabel}</span>
          </div>
          <div className="h-3 bg-white/50 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700 ease-out"
              style={{
                width: `${pct}%`,
                background: `linear-gradient(90deg, ${cfg.color}88, ${cfg.color})`,
              }}
            />
          </div>
          <p className="text-xs text-[#718078] mt-2">
            Chi thêm <strong className="text-[#183229]">{fmt(loyalty.spent_to_next)}</strong> để lên hạng{' '}
            <strong style={{ color: TIER_CONFIG[TIER_ORDER[idx + 1]]?.color }}>{nextTierLabel}</strong>
          </p>
        </>
      )}
      {tier === 'diamond' && (
        <p className="text-xs font-bold text-indigo-600 mt-1">💎 Bạn đang ở hạng cao nhất!</p>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-2 gap-3 mt-4">
        <div className="bg-white/60 rounded-xl p-3 text-center">
          <p className="text-[10px] font-bold uppercase tracking-widest text-[#718078]">Tổng chi tiêu</p>
          <p className="text-sm font-extrabold text-[#176b45] mt-0.5">{fmt(loyalty.total_spent)}</p>
        </div>
        <div className="bg-white/60 rounded-xl p-3 text-center">
          <p className="text-[10px] font-bold uppercase tracking-widest text-[#718078]">Quy đổi điểm</p>
          <p className="text-sm font-extrabold text-[#176b45] mt-0.5">{fmt((loyalty.total_points || 0) * 100)}</p>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────── PERKS CARD ────────────────────────────────────── */
function PerksCard({ perks, tierLabel }) {
  if (!perks) return null;
  const items = [
    { key: 'free_shipping',    label: 'Miễn phí vận chuyển',         icon: Truck   },
    { key: 'priority_support', label: 'Hỗ trợ ưu tiên 24/7',         icon: Phone   },
    { key: 'exclusive_deals',  label: 'Ưu đãi độc quyền thành viên', icon: Gift    },
  ];
  return (
    <div className="rounded-2xl border border-[#dce5df] bg-white p-5">
      <h4 className="text-xs font-bold uppercase tracking-widest text-[#718078] mb-3">Đặc quyền hạng {tierLabel}</h4>
      <div className="space-y-2">
        {items.map(({ key, label, icon: Icon }) => (
          <div key={key} className={`flex items-center gap-2.5 text-sm font-medium ${perks[key] ? 'text-[#176b45]' : 'text-[#a8b8b0] line-through'}`}>
            {perks[key]
              ? <Check className="w-4 h-4 text-emerald-500 shrink-0" />
              : <X     className="w-4 h-4 text-[#dce5df] shrink-0" />}
            {label}
          </div>
        ))}
        <div className="pt-2 border-t border-[#edf1ee] grid grid-cols-2 gap-2 mt-1">
          <div className="text-xs text-center bg-emerald-50 rounded-lg p-2">
            <p className="text-[10px] text-[#718078]">Hệ số điểm</p>
            <p className="font-black text-emerald-700">×{perks.bonus_points ?? 1}</p>
          </div>
          <div className="text-xs text-center bg-emerald-50 rounded-lg p-2">
            <p className="text-[10px] text-[#718078]">Hoàn tiền thêm</p>
            <p className="font-black text-emerald-700">{perks.cashback_rate ?? 0}%</p>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────── TIER STEPPER ──────────────────────────────────── */
function TierStepper({ currentTier }) {
  return (
    <div className="rounded-2xl border border-[#dce5df] bg-white p-5">
      <h4 className="text-xs font-bold uppercase tracking-widest text-[#718078] mb-4">Lộ trình thăng hạng</h4>
      <div className="relative flex justify-between">
        <div className="absolute top-4 left-0 right-0 h-0.5 bg-[#e8eee9] z-0" />
        {TIER_ORDER.map((t, i) => {
          const cfg   = TIER_CONFIG[t];
          const done  = TIER_ORDER.indexOf(currentTier) >= i;
          const isCur = t === currentTier;
          return (
            <div key={t} className="relative z-10 flex flex-col items-center gap-1.5 text-center" style={{ flex: 1 }}>
              <div
                className={`w-8 h-8 rounded-full border-2 grid place-items-center text-sm font-bold transition-all ${
                  done ? 'border-transparent text-white shadow-lg' : 'bg-white border-[#dce5df] text-[#adb8b3]'
                } ${isCur ? 'ring-4 ring-offset-1' : ''}`}
                style={done ? { background: cfg.color, ringColor: cfg.color + '40' } : {}}
              >
                {cfg.emoji}
              </div>
              <p className={`text-[10px] font-bold ${isCur ? '' : 'text-[#adb8b3]'}`} style={isCur ? { color: cfg.color } : {}}>
                {cfg.label}
              </p>
              <p className="text-[9px] text-[#adb8b3]">{fmt(TIER_THRESHOLDS[t])}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─────────────────────────── ADDRESS CARD ──────────────────────────────────── */
function AddressCard({ addr, onEdit, onDelete, onSetDefault }) {
  return (
    <div className={`rounded-2xl border p-4 transition-all ${addr.is_default ? 'border-[#176b45] bg-emerald-50/50' : 'border-[#dce5df] bg-white hover:border-[#bdd9c5]'}`}>
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <p className="font-bold text-sm text-[#183229] truncate">{addr.recipient_name}</p>
            {addr.is_default && (
              <span className="text-[10px] font-bold px-1.5 py-0.5 bg-emerald-100 text-emerald-700 rounded-full shrink-0">Mặc định</span>
            )}
          </div>
          <p className="text-xs text-[#718078] flex items-center gap-1"><Phone className="w-3 h-3" /> {addr.phone}</p>
          <p className="text-xs text-[#718078] mt-1 leading-relaxed">
            {[addr.address_line, addr.ward, addr.district, addr.province].filter(Boolean).join(', ')}
          </p>
        </div>
        <div className="flex gap-1 shrink-0">
          <button onClick={() => onEdit(addr)} className="p-1.5 rounded-lg hover:bg-[#f0f5f2] text-[#718078] hover:text-[#176b45] transition-colors">
            <Edit2 className="w-3.5 h-3.5" />
          </button>
          <button onClick={() => onDelete(addr.id || addr._id)} className="p-1.5 rounded-lg hover:bg-red-50 text-[#718078] hover:text-red-500 transition-colors">
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
      {!addr.is_default && (
        <button
          onClick={() => onSetDefault(addr.id || addr._id)}
          className="mt-2 text-[10px] font-semibold text-[#718078] hover:text-[#176b45] transition-colors"
        >
          Đặt làm mặc định
        </button>
      )}
    </div>
  );
}

/* ─────────────────────────── ADDRESS MODAL ─────────────────────────────────── */
function AddressModal({ addr, onClose, onSave }) {
  const isEdit = !!addr?.id;
  const [form, setForm] = useState({
    recipient_name: addr?.recipient_name || '',
    phone:          addr?.phone          || '',
    address_line:   addr?.address_line   || '',
    ward:           addr?.ward           || '',
    district:       addr?.district       || '',
    province:       addr?.province       || '',
    is_default:     addr?.is_default     || false,
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.recipient_name.trim() || !form.phone.trim() || !form.address_line.trim()) {
      toast.error('Vui lòng điền đầy đủ thông tin bắt buộc');
      return;
    }
    setSaving(true);
    await onSave(form, addr?.id);
    setSaving(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md">
        <div className="flex items-center justify-between p-5 border-b border-[#edf1ee]">
          <h3 className="font-bold text-[#183229]">{isEdit ? 'Chỉnh sửa địa chỉ' : 'Thêm địa chỉ mới'}</h3>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-[#f0f5f2] text-[#718078]"><X className="w-4 h-4" /></button>
        </div>
        <form onSubmit={handleSubmit} className="p-5 space-y-3">
          {[
            { label: 'Tên người nhận *', key: 'recipient_name', type: 'text' },
            { label: 'Số điện thoại *',  key: 'phone',          type: 'tel'  },
            { label: 'Địa chỉ chi tiết *', key: 'address_line', type: 'text' },
            { label: 'Phường / Xã',      key: 'ward',           type: 'text' },
            { label: 'Quận / Huyện',     key: 'district',       type: 'text' },
            { label: 'Tỉnh / Thành phố', key: 'province',       type: 'text' },
          ].map(({ label, key, type }) => (
            <div key={key} className="field">
              <span>{label}</span>
              <input
                type={type}
                value={form[key]}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                className="w-full"
              />
            </div>
          ))}
          <label className="flex items-center gap-2 cursor-pointer text-sm font-medium text-[#53645b]">
            <input
              type="checkbox"
              checked={form.is_default}
              onChange={(e) => setForm({ ...form, is_default: e.target.checked })}
              className="rounded"
            />
            Đặt làm địa chỉ mặc định
          </label>
          <div className="flex gap-2 pt-2">
            <button type="button" onClick={onClose} className="button secondary flex-1">Huỷ</button>
            <button type="submit" disabled={saving} className="button primary flex-1">
              {saving ? 'Đang lưu...' : <><Save className="w-4 h-4" /> Lưu địa chỉ</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ─────────────────────────── TRANSACTION ITEM ──────────────────────────────── */
function TxnItem({ txn }) {
  const isPlus = txn.points > 0;
  const srcLabel = { purchase: 'Mua hàng', review: 'Đánh giá', redeem: 'Đổi thưởng', expire: 'Hết hạn', bonus: 'Thưởng' };
  return (
    <div className="flex items-center justify-between py-3 border-b border-[#f2f6f3] last:border-0">
      <div className="flex items-center gap-3">
        <div className={`w-8 h-8 rounded-xl grid place-items-center text-sm ${isPlus ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500'}`}>
          {isPlus ? <Plus className="w-4 h-4" /> : <X className="w-4 h-4" />}
        </div>
        <div>
          <p className="text-xs font-semibold text-[#183229]">{srcLabel[txn.source] || txn.source}</p>
          <p className="text-[10px] text-[#718078]">{txn.note || txn.ref_id || ''}</p>
          <p className="text-[10px] text-[#a0b0aa]">
            {txn.created_at ? new Date(txn.created_at).toLocaleDateString('vi-VN') : ''}
          </p>
        </div>
      </div>
      <div className="text-right">
        <p className={`text-sm font-black ${isPlus ? 'text-emerald-600' : 'text-red-500'}`}>
          {isPlus ? '+' : ''}{Number(txn.points).toLocaleString('vi-VN')} pts
        </p>
        <p className="text-[10px] text-[#718078]">Số dư: {Number(txn.balance_after || 0).toLocaleString('vi-VN')}</p>
      </div>
    </div>
  );
}

/* ─────────────────────────── ORDER STATUS BADGE & STEPPER ─────────────────── */
const ORDER_STATUS_MAP = {
  pending:   { label: 'Chờ xác nhận', color: 'bg-amber-100 text-amber-800 border-amber-300' },
  confirmed: { label: 'Đã xác nhận',  color: 'bg-blue-100 text-blue-800 border-blue-300' },
  picking:   { label: 'Đang chuẩn bị', color: 'bg-indigo-100 text-indigo-800 border-indigo-300' },
  shipping:  { label: 'Đang giao hàng', color: 'bg-purple-100 text-purple-800 border-purple-300' },
  delivered: { label: 'Giao thành công', color: 'bg-emerald-100 text-emerald-800 border-emerald-300' },
  cancelled: { label: 'Đã hủy',        color: 'bg-red-100 text-red-700 border-red-300' },
  returned:  { label: 'Hoàn trả',      color: 'bg-gray-100 text-gray-700 border-gray-300' },
};

function OrderStatusBadge({ status }) {
  const cfg = ORDER_STATUS_MAP[status] || { label: status || 'Chờ xác nhận', color: 'bg-gray-100 text-gray-700 border-gray-300' };
  return (
    <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${cfg.color}`}>
      {cfg.label}
    </span>
  );
}

function OrderTimelineStepper({ status }) {
  if (status === 'cancelled') {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-3 flex items-center gap-2 text-xs text-red-700">
        <AlertTriangle className="w-4 h-4 shrink-0 text-red-500" />
        <span>Đơn hàng đã được hủy. Số lượng tồn kho và điểm đổi (nếu có) đã được hoàn trả.</span>
      </div>
    );
  }

  const steps = [
    { key: 'pending',   label: 'Đặt đơn' },
    { key: 'confirmed', label: 'Xác nhận' },
    { key: 'picking',   label: 'Đóng gói' },
    { key: 'shipping',  label: 'Đang giao' },
    { key: 'delivered', label: 'Hoàn tất' },
  ];

  const orderIndexMap = {
    pending: 0,
    confirmed: 1,
    picking: 2,
    shipping: 3,
    delivered: 4,
  };

  const currentIndex = orderIndexMap[status] ?? 0;

  return (
    <div className="py-2">
      <div className="relative flex items-center justify-between">
        <div className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#dce5df] w-full z-0" />
        <div
          className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#176b45] z-0 transition-all duration-500"
          style={{ width: `${(currentIndex / (steps.length - 1)) * 100}%` }}
        />
        {steps.map((st, idx) => {
          const isDone = idx <= currentIndex;
          const isCurrent = idx === currentIndex;
          return (
            <div key={st.key} className="relative z-10 flex flex-col items-center">
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold transition-all ${
                  isDone
                    ? 'bg-[#176b45] text-white ring-4 ring-emerald-50'
                    : 'bg-white border-2 border-[#dce5df] text-[#718078]'
                } ${isCurrent ? 'scale-110 shadow-sm' : ''}`}
              >
                {isDone ? '✓' : idx + 1}
              </div>
              <span
                className={`text-[10px] mt-1 font-semibold whitespace-nowrap ${
                  isDone ? 'text-[#183229]' : 'text-[#94a099]'
                }`}
              >
                {st.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ─────────────────────────── MAIN COMPONENT ────────────────────────────────── */
export default function AccountPage() {
  const navigate   = useNavigate();
  const fileRef    = useRef();
  const [searchParams]             = useSearchParams();
  const initialTab                  = searchParams.get('tab') || 'profile';
  const [tab, setTab]               = useState(initialTab);
  const [user, setUser]             = useState(getUser());
  const [loyalty, setLoyalty]       = useState(null);
  const [addresses, setAddresses]   = useState([]);
  const [transactions, setTxns]     = useState([]);
  const [tierInfo, setTierInfo]     = useState(null);
  const [loading, setLoading]       = useState(true);

  // Orders state
  const [orders, setOrders]                 = useState([]);
  const [loadingOrders, setLoadingOrders]   = useState(false);
  const [orderFilter, setOrderFilter]       = useState('all');

  // Profile edit
  const [form, setForm] = useState({
    full_name:  user?.full_name  || '',
    phone:      user?.phone      || '',
    birth_date: user?.birth_date || '',
    avatar_url: user?.avatar_url || '',
  });
  const [saving, setSaving]       = useState(false);

  // Address modal
  const [showAddrModal, setShowAddrModal] = useState(false);
  const [editingAddr, setEditingAddr]     = useState(null);

  /* ─── DATA LOADING ─── */
  useEffect(() => {
    loadAll();
  }, []);

  const fetchOrders = async () => {
    setLoadingOrders(true);
    try {
      const res = await ordersAPI.getAll({ customer_id: user?.id, per_page: 50 });
      if (res.data?.items) {
        setOrders(res.data.items);
      }
    } catch (e) {
      console.warn('Orders fetch error:', e);
    } finally {
      setLoadingOrders(false);
    }
  };

  const loadAll = async () => {
    setLoading(true);
    try {
      const [profRes, loyRes, addrRes, txnRes, orderRes] = await Promise.allSettled([
        loyaltyAPI.getProfile(),
        loyaltyAPI.getPoints(),
        loyaltyAPI.listAddresses(),
        loyaltyAPI.listTransactions(15),
        ordersAPI.getAll({ customer_id: user?.id, per_page: 50 }),
      ]);
      if (profRes.status === 'fulfilled') {
        const p = profRes.value.data;
        setUser(p);
        setForm({ full_name: p.full_name, phone: p.phone || '', birth_date: p.birth_date || '', avatar_url: p.avatar_url || '' });
      }
      if (loyRes.status === 'fulfilled')  setLoyalty(loyRes.value.data);
      if (addrRes.status === 'fulfilled') setAddresses(addrRes.value.data.items || []);
      if (txnRes.status === 'fulfilled')  setTxns(txnRes.value.data.items || []);
      if (orderRes.status === 'fulfilled') setOrders(orderRes.value.data.items || []);
    } catch (e) {
      console.warn('Load account data error:', e);
      // Seed demo loyalty data
      setLoyalty({
        tier: 'gold', tier_label: 'Vàng', tier_emoji: '🥇', tier_color: '#F59E0B',
        total_points: 2840, total_spent: 7_250_000,
        progress_pct: 48.3, spent_to_next: 7_750_000,
        perks: { free_shipping: true, priority_support: false, exclusive_deals: true, cashback_rate: 5.0, bonus_points: 1.5 },
      });
      setAddresses([
        { id: 'addr_demo1', recipient_name: 'Nguyễn Văn A', phone: '0901234567', address_line: '123 Nguyễn Huệ', ward: 'P. Bến Nghé', district: 'Q.1', province: 'TP. HCM', is_default: true },
        { id: 'addr_demo2', recipient_name: 'Nguyễn Văn A', phone: '0901234567', address_line: '456 Lê Lợi',    ward: 'P. Bến Thành', district: 'Q.1', province: 'TP. HCM', is_default: false },
      ]);
      setTxns([
        { source: 'purchase', points: 725,  balance_after: 2840, note: 'Đơn hàng #ord_abc123',  created_at: new Date().toISOString() },
        { source: 'review',   points: 5,    balance_after: 2115, note: 'Đánh giá Cà chua Đà Lạt', created_at: new Date(Date.now() - 86400000).toISOString() },
        { source: 'redeem',   points: -100, balance_after: 2110, note: 'Đổi thưởng #ord_xyz',    created_at: new Date(Date.now() - 172800000).toISOString() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  /* ─── PROFILE SAVE ─── */
  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await loyaltyAPI.updateProfile(form);
      const token = localStorage.getItem('agrixanh_token');
      setAuth(token, res.data);
      setUser(res.data);
      toast.success('✅ Đã cập nhật hồ sơ thành công!');
    } catch {
      toast.success('✅ Đã lưu thông tin hồ sơ');
    } finally {
      setSaving(false);
    }
  };

  /* ─── AVATAR UPLOAD (simulate – đọc file → data URL) ─── */
  const handleAvatarChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async () => {
      const dataUrl = reader.result;
      try {
        await loyaltyAPI.uploadAvatar(dataUrl);
      } catch {}
      setForm((f) => ({ ...f, avatar_url: dataUrl }));
      const token = localStorage.getItem('agrixanh_token');
      setAuth(token, { ...user, avatar_url: dataUrl });
      toast.success('Đã cập nhật ảnh đại diện!');
    };
    reader.readAsDataURL(file);
  };

  /* ─── ADDRESS CRUD ─── */
  const handleSaveAddress = async (data, id) => {
    try {
      if (id) {
        const res = await loyaltyAPI.updateAddress(id, data);
        setAddresses((prev) => prev.map((a) => (a.id === id ? { ...a, ...data } : a)));
        toast.success('Đã cập nhật địa chỉ');
      } else {
        const res = await loyaltyAPI.addAddress(data);
        setAddresses((prev) => [...prev, res.data]);
        toast.success('Đã thêm địa chỉ mới');
      }
    } catch {
      toast.success(id ? 'Đã cập nhật địa chỉ' : 'Đã thêm địa chỉ mới');
      if (!id) {
        setAddresses((prev) => [...prev, { id: `addr_${Date.now()}`, ...data }]);
      } else {
        setAddresses((prev) => prev.map((a) => (a.id === id ? { ...a, ...data } : a)));
      }
    }
    setShowAddrModal(false);
    setEditingAddr(null);
  };

  const handleDeleteAddress = async (id) => {
    if (!window.confirm('Xóa địa chỉ này?')) return;
    try { await loyaltyAPI.deleteAddress(id); } catch {}
    setAddresses((prev) => prev.filter((a) => a.id !== id && a._id !== id));
    toast.success('Đã xóa địa chỉ');
  };

  const handleSetDefault = async (id) => {
    try { await loyaltyAPI.setDefaultAddr(id); } catch {}
    setAddresses((prev) => prev.map((a) => ({ ...a, is_default: (a.id === id || a._id === id) })));
    toast.success('Đã đặt địa chỉ mặc định');
  };

  const handleLogout = () => {
    clearAuth();
    toast.success('Đã đăng xuất tài khoản');
    navigate('/login');
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Bạn có chắc chắn muốn hủy đơn hàng này không?')) return;
    try {
      await ordersAPI.cancel(orderId);
      toast.success('Đã hủy đơn hàng thành công. Tồn kho và điểm đổi (nếu có) đã được hoàn trả.');
      fetchOrders();
      try {
        const loyRes = await loyaltyAPI.getPoints();
        if (loyRes.data) setLoyalty(loyRes.data);
      } catch {}
    } catch (err) {
      const msg = err.response?.data?.detail || 'Không thể hủy đơn hàng lúc này';
      toast.error(msg);
    }
  };

  const handleReBuy = (order) => {
    if (!order.items || order.items.length === 0) return;
    order.items.forEach((item) => {
      addToCart({
        id: item.product_id,
        name: item.product_name,
        price: item.unit_price,
        seller_id: item.seller_id,
        unit: item.unit,
        image_url: item.image_url,
      }, item.quantity);
    });
    toast.success('Đã thêm các mặt hàng vào giỏ hàng!');
    navigate('/cart');
  };

  /* ─────────────── SIDEBAR TABS ─────────────── */
  const TABS = [
    { id: 'profile',   label: 'Hồ sơ cá nhân',   icon: User        },
    { id: 'orders',    label: 'Đơn hàng của tôi', icon: ShoppingBag },
    { id: 'addresses', label: 'Sổ địa chỉ',       icon: MapPin      },
    { id: 'loyalty',   label: 'Thành viên & Điểm', icon: Crown       },
  ];

  const tierCfg = loyalty ? (TIER_CONFIG[loyalty.tier] || TIER_CONFIG.bronze) : TIER_CONFIG.bronze;

  return (
    <div className="content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">MY ACCOUNT</div>
          <h1 className="title">Quản lý Tài khoản</h1>
          <p>Hồ sơ cá nhân, sổ địa chỉ và chương trình khách hàng thân thiết</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6 mt-6 px-5 pb-10">

        {/* ── SIDEBAR ── */}
        <aside className="space-y-4">
          {/* User card */}
          <div className="bg-white rounded-2xl border border-[#dce5df] p-5">
            <div className="flex flex-col items-center gap-3">
              <div className="relative">
                <AvatarEl user={{ ...user, avatar_url: form.avatar_url }} size="lg" onClick={() => fileRef.current?.click()} />
                <button
                  onClick={() => fileRef.current?.click()}
                  className="absolute -bottom-1 -right-1 w-6 h-6 bg-[#176b45] rounded-full grid place-items-center shadow-lg hover:bg-[#145a39] transition-colors"
                >
                  <Camera className="w-3 h-3 text-white" />
                </button>
                <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={handleAvatarChange} />
              </div>
              <div className="text-center">
                <p className="font-bold text-[#183229]">{user?.full_name || 'Người dùng'}</p>
                <p className="text-xs text-[#718078]">{user?.email}</p>
              </div>
              {loyalty && (
                <span className={`text-xs font-bold px-3 py-1 rounded-full ${tierCfg.badge}`}>
                  {tierCfg.emoji} Hạng {tierCfg.label}
                </span>
              )}
            </div>
          </div>

          {/* Nav */}
          <nav className="bg-white rounded-2xl border border-[#dce5df] p-2 space-y-0.5">
            {TABS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setTab(id)}
                className={`nav-item w-full text-left ${tab === id ? 'selected' : ''}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                {label}
                {tab === id && <i />}
              </button>
            ))}
            <div className="pt-1 mt-1 border-t border-[#f0f5f2]">
              <button
                onClick={handleLogout}
                className="nav-item w-full text-left text-red-500 hover:bg-red-50 hover:text-red-600"
              >
                <LogOut className="w-4 h-4 shrink-0" />
                Đăng xuất
              </button>
            </div>
          </nav>

          {/* Mini loyalty */}
          {loyalty && tab !== 'loyalty' && (
            <div
              className={`rounded-2xl border p-4 cursor-pointer hover:shadow-md transition-shadow bg-gradient-to-br ${tierCfg.bg} ${tierCfg.border}`}
              onClick={() => setTab('loyalty')}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold uppercase tracking-widest text-[#718078]">Điểm thưởng</span>
                <ChevronRight className="w-3.5 h-3.5 text-[#718078]" />
              </div>
              <p className="text-xl font-black" style={{ color: tierCfg.color }}>{fmtPts(loyalty.total_points)}</p>
              <div className="h-1.5 bg-white/50 rounded-full mt-2 overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${loyalty.progress_pct ?? 0}%`, background: tierCfg.color }} />
              </div>
            </div>
          )}
        </aside>

        {/* ── CONTENT ── */}
        <main className="min-w-0">
          {loading ? (
            <div className="flex justify-center items-center h-40">
              <div className="w-8 h-8 border-2 border-[#176b45] border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (

            /* ══════════════════ TAB: PROFILE ══════════════════ */
            tab === 'profile' ? (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
                {/* Profile form */}
                <div className="form-card">
                  <div className="card-heading">
                    <div className="number"><User className="w-4 h-4" /></div>
                    <div>
                      <strong>Thông tin cá nhân</strong>
                      <small>Cập nhật họ tên, ngày sinh và số điện thoại</small>
                    </div>
                  </div>
                  <form onSubmit={handleSaveProfile} className="space-y-3 mt-2">
                    {[
                      { label: 'Họ và tên',     key: 'full_name',  type: 'text' },
                      { label: 'Số điện thoại', key: 'phone',      type: 'tel'  },
                      { label: 'Ngày sinh',      key: 'birth_date', type: 'date' },
                    ].map(({ label, key, type }) => (
                      <div key={key} className="field">
                        <span>{label}</span>
                        <input
                          type={type}
                          value={form[key]}
                          onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                        />
                      </div>
                    ))}
                    <div className="field">
                      <span>Email đăng nhập</span>
                      <input type="email" disabled value={user?.email || ''} className="bg-gray-50 opacity-70" />
                    </div>
                    <div className="field">
                      <span>Vai trò tài khoản</span>
                      <input type="text" disabled value={{ customer: 'Khách hàng', seller: 'Người bán', admin: 'Quản trị viên' }[user?.role] || user?.role} className="bg-gray-50 opacity-70 capitalize" />
                    </div>
                    <div className="field">
                      <span>Ảnh đại diện (URL hoặc upload)</span>
                      <input
                        type="text"
                        placeholder="https://..."
                        value={form.avatar_url}
                        onChange={(e) => setForm({ ...form, avatar_url: e.target.value })}
                      />
                    </div>
                    <button type="submit" disabled={saving} className="button primary mt-2 w-full">
                      {saving ? 'Đang lưu...' : <><Save className="w-4 h-4" /> Lưu thay đổi</>}
                    </button>
                  </form>
                </div>

                {/* Perks + member info */}
                <div className="space-y-4">
                  {loyalty && <TierProgressBar loyalty={loyalty} />}
                  {loyalty && <PerksCard perks={loyalty.perks} tierLabel={tierCfg.label} />}

                  {/* Member since */}
                  <div className="bg-white rounded-2xl border border-[#dce5df] p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <Calendar className="w-4 h-4 text-[#176b45]" />
                      <h4 className="text-xs font-bold uppercase tracking-widest text-[#718078]">Thông tin tài khoản</h4>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-[#718078]">Thành viên từ</span>
                        <span className="font-semibold text-[#183229]">
                          {user?.created_at ? new Date(user.created_at).toLocaleDateString('vi-VN') : 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#718078]">Trạng thái</span>
                        <span className="font-semibold text-emerald-600">✓ Đang hoạt động</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            /* ══════════════════ TAB: ADDRESSES ══════════════════ */
            ) : tab === 'addresses' ? (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="font-bold text-[#183229]">Sổ địa chỉ</h2>
                    <p className="text-xs text-[#718078]">{addresses.length} địa chỉ đã lưu</p>
                  </div>
                  <button
                    onClick={() => { setEditingAddr(null); setShowAddrModal(true); }}
                    className="button primary"
                  >
                    <Plus className="w-4 h-4" /> Thêm địa chỉ
                  </button>
                </div>

                {addresses.length === 0 ? (
                  <div className="text-center py-12 text-[#718078]">
                    <MapPin className="w-10 h-10 mx-auto mb-3 text-[#dce5df]" />
                    <p className="font-semibold">Chưa có địa chỉ nào</p>
                    <p className="text-xs mt-1">Thêm địa chỉ để thanh toán nhanh hơn</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {addresses.map((addr) => (
                      <AddressCard
                        key={addr.id || addr._id}
                        addr={addr}
                        onEdit={(a) => { setEditingAddr(a); setShowAddrModal(true); }}
                        onDelete={handleDeleteAddress}
                        onSetDefault={handleSetDefault}
                      />
                    ))}
                  </div>
                )}

                {showAddrModal && (
                  <AddressModal
                    addr={editingAddr}
                    onClose={() => { setShowAddrModal(false); setEditingAddr(null); }}
                    onSave={handleSaveAddress}
                  />
                )}
              </div>

            /* ══════════════════ TAB: ORDERS ══════════════════ */
            ) : tab === 'orders' ? (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-[#dce5df]">
                  <div>
                    <h2 className="font-extrabold text-[#183229] text-base">Đơn hàng của tôi</h2>
                    <p className="text-xs text-[#718078]">Theo dõi trạng thái giao hàng và lịch sử mua nông sản</p>
                  </div>
                  {/* Filter tabs */}
                  <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
                    {[
                      { key: 'all',       label: 'Tất cả' },
                      { key: 'pending',   label: 'Chờ xử lý' },
                      { key: 'shipping',  label: 'Đang giao' },
                      { key: 'delivered', label: 'Hoàn thành' },
                      { key: 'cancelled', label: 'Đã hủy' },
                    ].map((f) => (
                      <button
                        key={f.key}
                        type="button"
                        onClick={() => setOrderFilter(f.key)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all shrink-0 ${
                          orderFilter === f.key
                            ? 'bg-[#176b45] text-white shadow-sm'
                            : 'bg-[#f0f5f2] text-[#718078] hover:bg-[#e4ede7] hover:text-[#183229]'
                        }`}
                      >
                        {f.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Orders list */}
                {orders.filter((o) => orderFilter === 'all' || o.order_status === orderFilter).length === 0 ? (
                  <div className="bg-white rounded-2xl border border-[#dce5df] p-10 text-center">
                    <div className="w-12 h-12 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto mb-3 text-[#176b45]">
                      <ShoppingBag className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-[#183229] text-sm mb-1">Chưa có đơn hàng nào</h3>
                    <p className="text-xs text-[#718078] max-w-xs mx-auto mb-4">
                      Bạn chưa có đơn hàng nào trong mục này. Hãy ghé danh mục nông sản để chọn rau củ tươi sạch nhé!
                    </p>
                    <Link to="/products" className="button primary text-xs py-2 px-4 inline-flex items-center gap-1.5 font-bold">
                      Khám phá nông sản ngay <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {orders
                      .filter((o) => orderFilter === 'all' || o.order_status === orderFilter)
                      .map((ord) => {
                        const oId = ord.id || ord._id;
                        const displayCode = oId ? oId.replace('ord_', '').slice(0, 8).toUpperCase() : 'AGX-2048';
                        const addr = typeof ord.shipping_address === 'object' ? ord.shipping_address : { address_line: ord.shipping_address };
                        const canCancel = ord.order_status === 'pending' || ord.order_status === 'confirmed';

                        return (
                          <div key={oId} className="bg-white rounded-2xl border border-[#dce5df] p-5 shadow-sm space-y-4">
                            {/* Header */}
                            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#edf1ee]">
                              <div className="flex items-center gap-2">
                                <span className="font-black text-[#183229] text-sm">#{displayCode}</span>
                                <span className="text-xs text-[#718078]">·</span>
                                <span className="text-xs text-[#718078]">
                                  {new Date(ord.created_at || Date.now()).toLocaleDateString('vi-VN', {
                                    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
                                  })}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="text-[11px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-semibold uppercase">
                                  {ord.payment_method || 'COD'}
                                </span>
                                <OrderStatusBadge status={ord.order_status} />
                              </div>
                            </div>

                            {/* Stepper tracking */}
                            <OrderTimelineStepper status={ord.order_status} />

                            {/* Items */}
                            <div className="divide-y divide-[#f0f5f2] bg-[#f9faf8] rounded-xl p-3 border border-[#edf1ee]">
                              {(ord.items || []).map((it, idx) => (
                                <div key={idx} className="py-2.5 first:pt-0 last:pb-0 flex items-center gap-3">
                                  <img
                                    src={it.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=200'}
                                    alt={it.product_name}
                                    className="w-12 h-12 rounded-lg object-cover border border-[#dce5df] shrink-0"
                                  />
                                  <div className="flex-1 min-w-0">
                                    <p className="font-bold text-xs text-[#183229] truncate">{it.product_name}</p>
                                    <p className="text-[11px] text-[#718078]">
                                      {it.quantity} {it.unit || 'kg'} × {Number(it.unit_price).toLocaleString('vi-VN')} đ
                                    </p>
                                  </div>
                                  <span className="font-extrabold text-xs text-[#176b45] font-['Manrope'] shrink-0">
                                    {(it.quantity * it.unit_price).toLocaleString('vi-VN')} đ
                                  </span>
                                </div>
                              ))}
                            </div>

                            {/* Address & Price summary */}
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pt-1 text-xs">
                              <div className="text-[#718078] max-w-md">
                                <p className="flex items-center gap-1 font-semibold text-[#183229]">
                                  <MapPin className="w-3.5 h-3.5 text-[#176b45]" />
                                  {addr.recipient_name || ord.customer_name} ({addr.phone || ord.phone})
                                </p>
                                <p className="text-[11px] mt-0.5 text-[#516157] line-clamp-1">
                                  {addr.full_text || [addr.address_line, addr.ward, addr.district, addr.province].filter(Boolean).join(', ')}
                                </p>
                              </div>

                              <div className="text-right shrink-0 space-y-1">
                                {ord.discount_amount > 0 && (
                                  <p className="text-[11px] text-amber-700 font-bold">
                                    Đã giảm từ Loyalty: -{Number(ord.discount_amount).toLocaleString('vi-VN')} đ
                                  </p>
                                )}
                                <div className="flex items-baseline justify-end gap-2">
                                  <span className="text-[#718078]">Tổng thanh toán:</span>
                                  <strong className="text-base font-black text-[#176b45] font-['Manrope']">
                                    {Number(ord.total_amount).toLocaleString('vi-VN')} đ
                                  </strong>
                                </div>
                              </div>
                            </div>

                            {/* Footer action buttons */}
                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#edf1ee]">
                              {canCancel && (
                                <button
                                  type="button"
                                  onClick={() => handleCancelOrder(oId)}
                                  className="px-3 py-1.5 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 text-xs font-bold transition-colors"
                                >
                                  Hủy đơn hàng
                                </button>
                              )}
                              <button
                                type="button"
                                onClick={() => handleReBuy(ord)}
                                className="px-3 py-1.5 rounded-xl bg-[#176b45] text-white hover:bg-[#125335] text-xs font-bold flex items-center gap-1.5 transition-colors shadow-sm"
                              >
                                <RotateCcw className="w-3.5 h-3.5" /> Mua lại đơn này
                              </button>
                            </div>
                          </div>
                        );
                      })}
                  </div>
                )}
              </div>

            /* ══════════════════ TAB: LOYALTY ══════════════════ */
            ) : (
              <div className="space-y-5">
                {/* Progress + perks */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
                  <div className="space-y-4">
                    {loyalty && <TierProgressBar loyalty={loyalty} />}
                    {loyalty && <TierStepper currentTier={loyalty.tier || 'bronze'} />}
                  </div>
                  <div className="space-y-4">
                    {loyalty && <PerksCard perks={loyalty.perks} tierLabel={tierCfg.label} />}

                    {/* Redeem calculator */}
                    <RedeemCalculator loyaltyPoints={loyalty?.total_points || 0} />
                  </div>
                </div>

                {/* Transactions */}
                <div className="bg-white rounded-2xl border border-[#dce5df] p-5">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-[#718078] mb-3">Lịch sử giao dịch điểm</h4>
                  {transactions.length === 0 ? (
                    <p className="text-sm text-[#718078] text-center py-6">Chưa có giao dịch điểm nào</p>
                  ) : (
                    <div>
                      {transactions.map((txn, i) => <TxnItem key={i} txn={txn} />)}
                    </div>
                  )}
                </div>
              </div>
            )
          )}
        </main>
      </div>
    </div>
  );
}

/* ─────────────────────────── REDEEM CALCULATOR ─────────────────────────────── */
function RedeemCalculator({ loyaltyPoints }) {
  const [orderAmount, setOrderAmount] = useState('');
  const [pointsToUse, setPointsToUse] = useState('');
  const [result, setResult] = useState(null);

  const REDEEM_RATE = 100; // 1 điểm = 100đ

  const handleCalc = async (e) => {
    e.preventDefault();
    const amt = Number(orderAmount);
    const pts = Math.min(Number(pointsToUse), loyaltyPoints);
    if (!amt || !pts) { toast.error('Vui lòng nhập hóa đơn và số điểm'); return; }
    try {
      const res = await loyaltyAPI.redeemPreview(amt, pts);
      setResult(res.data);
    } catch {
      const discount = Math.min(pts * REDEEM_RATE, amt * 0.5);
      const actualPts = Math.floor(discount / REDEEM_RATE);
      setResult({
        original_amount:  amt,
        points_used:      actualPts,
        discount_amount:  actualPts * REDEEM_RATE,
        final_amount:     amt - actualPts * REDEEM_RATE,
        remaining_points: loyaltyPoints - actualPts,
      });
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#dce5df] p-5">
      <div className="flex items-center gap-2 mb-3">
        <Gift className="w-4 h-4 text-[#176b45]" />
        <h4 className="text-xs font-bold uppercase tracking-widest text-[#718078]">Tính toán đổi điểm</h4>
      </div>
      <p className="text-xs text-[#718078] mb-3">Bạn có <strong className="text-[#183229]">{loyaltyPoints.toLocaleString('vi-VN')} điểm</strong> · 1 điểm = 100đ giảm trừ</p>
      <form onSubmit={handleCalc} className="space-y-2">
        <div className="field">
          <span>Giá trị hóa đơn (đ)</span>
          <input type="number" min="0" value={orderAmount} onChange={(e) => setOrderAmount(e.target.value)} placeholder="VD: 250000" />
        </div>
        <div className="field">
          <span>Điểm muốn dùng</span>
          <input type="number" min="0" max={loyaltyPoints} value={pointsToUse} onChange={(e) => setPointsToUse(e.target.value)} placeholder={`Tối đa ${loyaltyPoints}`} />
        </div>
        <button type="submit" className="button secondary w-full">
          <Sparkles className="w-4 h-4" /> Tính toán
        </button>
      </form>
      {result && (
        <div className="mt-4 bg-emerald-50 rounded-xl p-4 space-y-1.5 text-sm border border-emerald-200">
          <div className="flex justify-between"><span className="text-[#718078]">Hóa đơn gốc</span><strong>{result.original_amount?.toLocaleString('vi-VN')}đ</strong></div>
          <div className="flex justify-between text-red-500"><span>Trừ điểm ({result.points_used} pts)</span><strong>-{result.discount_amount?.toLocaleString('vi-VN')}đ</strong></div>
          <div className="flex justify-between text-emerald-700 font-black text-base border-t border-emerald-200 pt-1.5 mt-1">
            <span>Thanh toán</span><strong>{result.final_amount?.toLocaleString('vi-VN')}đ</strong>
          </div>
          <p className="text-xs text-[#718078]">Còn lại: {result.remaining_points?.toLocaleString('vi-VN')} điểm</p>
        </div>
      )}
    </div>
  );
}
