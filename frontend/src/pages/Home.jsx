import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { productsAPI } from '../services/api';
import { addToCart } from '../store/authStore';
import { Sparkles, Shield, Search, ArrowRight, Plus } from 'lucide-react';
import toast from 'react-hot-toast';

const fallbackProducts = [
  {
    id: 'f1',
    name: 'Cà chua chín mọng Đà Lạt',
    farm: 'Green Valley Farm',
    price: 45000,
    unit: '/ kg',
    ai_quality: 'Hạng 1',
    rating: '4.9',
    category: 'Rau củ',
    image_url: 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85',
  },
  {
    id: 'f2',
    name: 'Giỏ nông sản hữu cơ tổng hợp',
    farm: 'Sunny Fields Co.',
    price: 185000,
    unit: '/ giỏ',
    ai_quality: 'Hạng 1',
    rating: '5.0',
    category: 'Rau củ',
    image_url: 'https://images.unsplash.com/photo-1624668430039-0175a0fbf006?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'f3',
    name: 'Cà rốt giòn ngọt Mộc Châu',
    farm: 'Mekong Roots',
    price: 32000,
    unit: '/ kg',
    ai_quality: 'Hạng 2',
    rating: '4.8',
    category: 'Rau củ',
    image_url: 'https://images.unsplash.com/photo-1609842947419-ba4f04d5d60f?auto=format&fit=crop&w=900&q=85',
  },
  {
    id: 'f4',
    name: 'Hộp rau củ xanh mùa thu hoạch',
    farm: 'Green Valley Farm',
    price: 120000,
    unit: '/ hộp',
    ai_quality: 'Hạng 1',
    rating: '4.9',
    category: 'Rau củ',
    image_url: 'https://images.unsplash.com/photo-1723347101054-c246b0034f11?auto=format&fit=crop&w=900&q=85',
  },
];

export default function Home() {
  const [products, setProducts] = useState(fallbackProducts);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('All');
  const navigate = useNavigate();

  useEffect(() => {
    productsAPI.getAll({ per_page: 8 })
      .then((res) => {
        if (res.data?.items && res.data.items.length > 0) {
          const apiItems = res.data.items.map((item) => ({
            ...item,
            farm: item.farm_name || 'Green Valley Farm',
            unit: '/ ' + (item.unit || 'kg'),
            ai_quality: item.ai_quality || 'Hạng 1',
            rating: '4.9',
          }));
          setProducts(apiItems);
        }
      })
      .catch((err) => {
        console.warn('API error, using curated Figma products:', err);
      });
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/products');
    }
  };

  const handleQuickAdd = (e, product) => {
    e.stopPropagation();
    addToCart(product, 1);
    toast.success(`Đã thêm ${product.name} vào giỏ!`);
  };

  const filteredProducts = products.filter((p) => {
    if (selectedFilter === 'Vegetables') {
      return p.category?.toLowerCase().includes('rau') || p.category?.toLowerCase().includes('veg');
    }
    if (selectedFilter === 'Fruits') {
      return p.category?.toLowerCase().includes('trái') || p.category?.toLowerCase().includes('quả') || p.category?.toLowerCase().includes('fruit');
    }
    return true;
  });

  return (
    <div className="content">
      {/* Figma Hero Banner */}
      <section className="hero">
        <img
          src="https://images.unsplash.com/photo-1624668430039-0175a0fbf006?auto=format&fit=crop&w=1200&q=85"
          alt="Nông sản hữu cơ tươi ngon trong giỏ thu hoạch"
        />
        <div className="hero-overlay" />

        <div className="hero-content">
          <div className="hero-kicker">
            <Shield className="w-4 h-4 text-emerald-300" />
            <span>AI-verified freshness</span>
          </div>
          <h1 className="hero-title">
            Nông sản sạch,<br />
            chăm sóc tận tâm.
          </h1>
          <p>
            Mua trực tiếp nông sản từ nhà vườn, chất lượng và độ tươi được thẩm định minh bạch bằng công nghệ thị giác trí tuệ nhân tạo.
          </p>

          <form onSubmit={handleSearchSubmit} className="hero-search">
            <Search className="w-4 h-4 text-[#819087] ml-1" />
            <input
              type="text"
              placeholder="Tìm cà chua, cà rốt, nông trại..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="button">
              Tìm kiếm
            </button>
          </form>
        </div>

        {/* Floating Freshness Card */}
        <div className="freshness-card">
          <div className="score-ring">
            98<span>%</span>
          </div>
          <div>
            <strong>Cam kết độ tươi ngon</strong>
            <small>100% sản phẩm được AI kiểm tra khuyết tật</small>
          </div>
        </div>
      </section>

      {/* Categories Row */}
      <div className="section-row">
        <div>
          <div className="section-title">Danh mục nông sản</div>
          <p>Thực phẩm tươi sạch thiết yếu cho mọi gia đình</p>
        </div>
        <Link to="/products" className="text-button">
          Xem tất cả <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      <div className="categories">
        <div
          onClick={() => navigate('/products?category=Rau củ')}
          className="category hover:border-[#176b45] cursor-pointer"
        >
          <span className="category-icon">🍅</span>
          <div>
            <strong>Rau củ hữu cơ</strong>
            <small>Khám phá sản phẩm tươi sạch</small>
          </div>
          <ArrowRight className="w-4 h-4 text-[#718078]" />
        </div>

        <div
          onClick={() => navigate('/products?category=Trái cây')}
          className="category hover:border-[#176b45] cursor-pointer"
        >
          <span className="category-icon">🍊</span>
          <div>
            <strong>Trái cây theo mùa</strong>
            <small>Đặc sản vùng miền chín mọng</small>
          </div>
          <ArrowRight className="w-4 h-4 text-[#718078]" />
        </div>

        <div className="category-note">
          <Sparkles className="w-7 h-7 text-[#176b45]" />
          <div>
            <strong>Tại sao cần AI Quality?</strong>
            <small>Phân loại chuẩn hóa - Mua sắm an tâm tuyệt đối</small>
          </div>
        </div>
      </div>

      {/* Featured Products */}
      <div className="section-row">
        <div>
          <div className="section-title">Nông sản nổi bật tuần này</div>
          <p>Đỉnh cao độ tươi, xác thực bởi hệ thống AgriXanh AI</p>
        </div>
        <div className="filter-chips">
          <button
            className={selectedFilter === 'All' ? 'active' : ''}
            onClick={() => setSelectedFilter('All')}
          >
            Tất cả
          </button>
          <button
            className={selectedFilter === 'Vegetables' ? 'active' : ''}
            onClick={() => setSelectedFilter('Vegetables')}
          >
            Rau củ
          </button>
          <button
            className={selectedFilter === 'Fruits' ? 'active' : ''}
            onClick={() => setSelectedFilter('Fruits')}
          >
            Trái cây
          </button>
        </div>
      </div>

      <div className="product-grid">
        {filteredProducts.map((p) => (
          <article
            key={p.id}
            className="product-card"
            onClick={() => navigate(`/products/${p.id}`)}
          >
            <div className="product-photo">
              <img
                src={p.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85'}
                alt={p.name}
              />
              <div className="ai-badge">
                <Sparkles className="w-3.5 h-3.5 text-[#176b45]" />
                <span>AI Quality</span>
                <strong>{p.ai_quality || 'Grade 1'}</strong>
              </div>
              <button
                type="button"
                className="quick-add"
                title="Thêm nhanh vào giỏ"
                onClick={(e) => handleQuickAdd(e, p)}
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="product-info">
              <small>{p.farm || 'Nông trại Việt'}</small>
              <div className="product-name">{p.name}</div>
              <div className="product-bottom">
                <strong>{Number(p.price).toLocaleString('vi-VN')} đ</strong>
                <span>{p.unit || '/ kg'}</span>
                <div className="rating">★ {p.rating || '4.9'}</div>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
