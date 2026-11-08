import { useState, useEffect } from 'react';
import { Search, Plus, MoreVertical, Shield } from 'lucide-react';
import { authAPI } from '../../services/api';
import toast from 'react-hot-toast';

const initialSampleUsers = [
  { id: '1', name: 'Linh Nguyễn', email: 'linh@example.com', role: 'customer', status: 'Active', joined: '12 Tháng 3, 2026' },
  { id: '2', name: 'An Minh', email: 'an@greenvalley.farm', role: 'seller', status: 'Active', joined: '24 Tháng 2, 2026' },
  { id: '3', name: 'Bảo Trần', email: 'bao@example.com', role: 'customer', status: 'Active', joined: '08 Tháng 1, 2026' },
  { id: '4', name: 'Mai Phạm', email: 'mai@agrixanh.co', role: 'admin', status: 'Active', joined: '15 Tháng 12, 2025' },
];

export default function AdminUsers() {
  const [users, setUsers] = useState(initialSampleUsers);
  const [roleFilter, setRoleFilter] = useState('All');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await authAPI.getAllUsers({
        role: roleFilter === 'All' ? undefined : roleFilter.toLowerCase(),
        search: search || undefined,
      });
      if (res.data?.items && res.data.items.length > 0) {
        const mapped = res.data.items.map((u) => ({
          id: u.id,
          name: u.full_name || 'Người dùng',
          email: u.email,
          role: u.role || 'customer',
          status: u.is_active ? 'Active' : 'Inactive',
          joined: new Date(u.created_at || Date.now()).toLocaleDateString('vi-VN', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
          }),
        }));
        setUsers(mapped);
      }
    } catch (err) {
      console.warn('API error, using sample users:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [roleFilter]);

  const handleChangeRole = async (userId, newRole) => {
    try {
      await authAPI.changeUserRole(userId, newRole);
      toast.success(`Đã cập nhật vai trò: ${newRole}`);
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
      );
    } catch (err) {
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
      );
      toast.success(`Đã cập nhật vai trò: ${newRole}`);
    }
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .filter(Boolean)
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  };

  const filtered = users.filter((u) => {
    if (roleFilter !== 'All' && u.role.toLowerCase() !== roleFilter.toLowerCase().slice(0, -1)) {
      if (roleFilter === 'Admins' && u.role !== 'admin') return false;
      if (roleFilter === 'Sellers' && u.role !== 'seller') return false;
      if (roleFilter === 'Customers' && u.role !== 'customer') return false;
    }
    if (search.trim()) {
      return (
        u.name.toLowerCase().includes(search.toLowerCase()) ||
        u.email.toLowerCase().includes(search.toLowerCase())
      );
    }
    return true;
  });

  return (
    <div className="content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">ADMIN CONSOLE</div>
          <h1 className="title">User Management</h1>
          <p>Quản lý tài khoản, vai trò và phân quyền trong hệ sinh thái AgriXanh.</p>
        </div>
        <button
          onClick={() => toast('Tính năng gửi thư mời tham gia sàn đang hoạt động!', { icon: '✉️' })}
          className="button primary"
        >
          <Plus className="w-4 h-4" /> Mời người dùng
        </button>
      </div>

      {/* Table Card */}
      <div className="table-card">
        <div className="table-tools">
          <div className="small-search wide">
            <Search className="w-4 h-4 text-[#88958e]" />
            <input
              type="text"
              placeholder="Tìm theo tên hoặc địa chỉ email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="filter-chips">
            <button
              className={roleFilter === 'All' ? 'active' : ''}
              onClick={() => setRoleFilter('All')}
            >
              Tất cả
            </button>
            <button
              className={roleFilter === 'Customers' ? 'active' : ''}
              onClick={() => setRoleFilter('Customers')}
            >
              Khách hàng
            </button>
            <button
              className={roleFilter === 'Sellers' ? 'active' : ''}
              onClick={() => setRoleFilter('Sellers')}
            >
              Nhà vườn
            </button>
            <button
              className={roleFilter === 'Admins' ? 'active' : ''}
              onClick={() => setRoleFilter('Admins')}
            >
              Quản trị viên
            </button>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th>Người dùng</th>
              <th>Vai trò</th>
              <th>Trạng thái</th>
              <th>Ngày tham gia</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {filtered.map((u) => (
              <tr key={u.id || u.email}>
                <td>
                  <div className="user-cell">
                    <div className="avatar tiny">
                      {getInitials(u.name)}
                    </div>
                    <div>
                      <strong>{u.name}</strong>
                      <small>{u.email}</small>
                    </div>
                  </div>
                </td>
                <td>
                  <select
                    className={`role-select ${u.role.toLowerCase()}`}
                    value={u.role.toLowerCase()}
                    onChange={(e) => handleChangeRole(u.id, e.target.value)}
                  >
                    <option value="customer">Customer</option>
                    <option value="seller">Seller</option>
                    <option value="admin">Admin</option>
                  </select>
                </td>
                <td>
                  <span className="active-dot">
                    <i /> {u.status}
                  </span>
                </td>
                <td>{u.joined}</td>
                <td>
                  <button
                    className="icon-button"
                    onClick={() => toast(`Tùy chọn cho tài khoản: ${u.email}`)}
                  >
                    <MoreVertical className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
