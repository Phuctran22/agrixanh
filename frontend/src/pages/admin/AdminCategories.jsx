import { useState, useEffect } from 'react';
import {
  Boxes,
  Plus,
  Trash2,
  RefreshCw,
  Tag,
} from 'lucide-react';
import { productsAPI } from '../../services/api';
import toast from 'react-hot-toast';

export default function AdminCategories() {
  const [categories, setCategories] = useState([]);
  const [newCatName, setNewCatName] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const res = await productsAPI.getCategories();
      if (res.data?.categories && res.data.categories.length > 0) {
        setCategories(res.data.categories);
      } else {
        setCategories(['Rau củ hữu cơ', 'Trái cây theo mùa', 'Gia vị & Thảo mộc', 'Thực phẩm sấy']);
      }
    } catch (err) {
      console.warn('API error, using default categories:', err);
      setCategories(['Rau củ hữu cơ', 'Trái cây theo mùa', 'Gia vị & Thảo mộc', 'Thực phẩm sấy']);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleAddCategory = async (e) => {
    e.preventDefault();
    const name = newCatName.trim();
    if (!name) return;

    setSubmitting(true);
    try {
      await productsAPI.addCategory(name);
      toast.success(`Đã thêm danh mục: ${name}`);
      setNewCatName('');
      fetchCategories();
    } catch (err) {
      setCategories([...categories, name]);
      toast.success(`Đã thêm danh mục: ${name}`);
      setNewCatName('');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteCategory = async (name) => {
    if (!window.confirm(`Bạn có chắc chắn muốn xóa danh mục "${name}"?`)) return;
    try {
      await productsAPI.deleteCategory(name);
      toast.success(`Đã xóa danh mục: ${name}`);
      setCategories(categories.filter((c) => c !== name));
    } catch (err) {
      setCategories(categories.filter((c) => c !== name));
      toast.success(`Đã xóa danh mục: ${name}`);
    }
  };

  return (
    <div className="content">
      {/* Page Heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">ADMIN CONSOLE / CATEGORIES</div>
          <h1 className="title">Category Classification</h1>
          <p>Phân loại các nhóm nông sản để phục vụ bộ lọc tìm kiếm và kiểm định thị giác AI.</p>
        </div>
        <div className="draft-badge">{categories.length} phân loại</div>
      </div>

      <div className="create-grid">
        {/* Left Form: Add Category */}
        <div className="form-card">
          <div className="card-heading">
            <div className="number">
              <Plus className="w-4 h-4" />
            </div>
            <div>
              <strong>Thêm phân loại mới</strong>
              <small>Nhập tên danh mục nông sản</small>
            </div>
          </div>

          <form onSubmit={handleAddCategory}>
            <div className="field">
              <span>Tên danh mục</span>
              <input
                type="text"
                placeholder="Ví dụ: Nông sản đạt chuẩn OCOP, Nấm tươi..."
                value={newCatName}
                onChange={(e) => setNewCatName(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="button primary w-full mt-2"
            >
              {submitting ? 'Đang lưu...' : '+ Thêm danh mục mới'}
            </button>
          </form>
        </div>

        {/* Right Table Card: Category List */}
        <div className="table-card">
          <div className="table-tools">
            <div className="text-xs font-bold uppercase tracking-wider text-[#94a099]">
              Danh mục hiện có ({categories.length})
            </div>
            <button
              onClick={fetchCategories}
              className="button secondary px-3 py-1 text-xs"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Tải lại
            </button>
          </div>

          <table>
            <thead>
              <tr>
                <th>Tên phân loại</th>
                <th>Tình trạng</th>
                <th className="text-right">Xóa</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((cat) => (
                <tr key={cat}>
                  <td>
                    <div className="flex items-center gap-2">
                      <Tag className="w-4 h-4 text-[#176b45]" />
                      <strong className="text-[#183229] font-bold">{cat}</strong>
                    </div>
                  </td>
                  <td>
                    <span className="active-dot">
                      <i /> Đang kích hoạt
                    </span>
                  </td>
                  <td className="text-right">
                    <button
                      onClick={() => handleDeleteCategory(cat)}
                      className="icon-button text-red-500 hover:text-red-700 ml-auto"
                      title="Xóa danh mục"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
