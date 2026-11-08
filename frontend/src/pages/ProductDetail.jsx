import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Sparkles, Shield, Check, ShoppingBag, ArrowRight, Plus } from 'lucide-react';
import { productsAPI } from '../services/api';
import { addToCart } from '../store/authStore';
import toast from 'react-hot-toast';

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0);

  useEffect(() => {
    if (id) {
      productsAPI.getRelated(id, 4)
        .then((res) => {
          if (res.data?.items) setRelatedProducts(res.data.items);
        })
        .catch((err) => console.warn('Could not fetch related products:', err));
    }
  }, [id]);

  useEffect(() => {
    productsAPI
      .getById(id)
      .then((res) => {
        setProduct(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.warn('API fetch failed, using fallback product:', err);
        setProduct({
          id: id || 'p1',
          name: 'Cà chua chín mọng Đà Lạt',
          category: 'Rau củ',
          farm_name: 'Green Valley Farm',
          price: 45000,
          unit: 'kg',
          description: 'Cà chua chín cây hữu cơ, trồng theo phương pháp canh tác bền vững trên cao nguyên Đà Lạt. Vỏ căng bóng, vị ngọt đậm đà tự nhiên, chứa nhiều vitamin C và Lycopene.',
          ai_quality: 'Hạng 1',
          ai_confidence: 98.4,
          surface_condition: 'Mặt quả nhẵn, không có vết thâm nứt',
          color_consistency: 'Đỏ mọng đều 96%',
          image_url: 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85',
        });
        setLoading(false);
      });
  }, [id]);

  const handleAddToCart = () => {
    if (!product) return;
    addToCart(product, quantity);
    toast.success(`Đã thêm ${quantity} ${product.unit || 'kg'} vào giỏ hàng!`);
  };

  const handleBuyNow = () => {
    if (!product) return;
    addToCart(product, quantity);
    navigate('/cart');
  };

  if (loading) {
    return (
      <div className="content text-center py-20">
        <div className="w-10 h-10 border-4 border-[#176b45] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-[#718078]">Đang tải chi tiết nông sản & kiểm định AI...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="content text-center py-20">
        <h2 className="title mb-3">Không tìm thấy nông sản</h2>
        <Link to="/products" className="button primary">
          Quay lại sàn nông sản
        </Link>
      </div>
    );
  }

  const galleryImages = [
    product.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85',
    'https://images.unsplash.com/photo-1624668430039-0175a0fbf006?auto=format&fit=crop&w=1200&q=85',
    'https://images.unsplash.com/photo-1723347101054-c246b0034f11?auto=format&fit=crop&w=900&q=85',
  ];

  return (
    <div className="content">
      {/* Back button */}
      <Link to="/products" className="back">
        ← Quay lại sàn nông sản
      </Link>

      <div className="detail-layout">
        {/* Gallery */}
        <div className="gallery">
          <div className="main-image">
            <img
              src={galleryImages[selectedPhotoIndex] || galleryImages[0]}
              alt={product.name}
            />
            <div className="ai-badge large">
              <Sparkles className="w-4 h-4 text-[#176b45]" />
              <span>AI inspected · Đã kiểm định độ tươi</span>
            </div>
          </div>

          <div className="thumbs">
            {galleryImages.map((img, i) => (
              <img
                key={i}
                src={img}
                alt={`Thumbnail ${i}`}
                className={selectedPhotoIndex === i ? 'active' : ''}
                onClick={() => setSelectedPhotoIndex(i)}
              />
            ))}
          </div>
        </div>

        {/* Detail Info */}
        <div className="detail-info">
          <div className="eyebrow">
            {product.farm_name || 'Green Valley Farm'} · {product.category || 'Nông sản hữu cơ'}
          </div>
          <h1 className="detail-title">{product.name}</h1>
          <div className="detail-rating">
            ★ 4.9 <span>126 đánh giá</span> <i /> <span>312 đã bán</span>
          </div>

          <div className="detail-price">
            {Number(product.price).toLocaleString('vi-VN')} đ{' '}
            <span>/ {product.unit || 'kg'}</span>
          </div>

          <p>{product.description || 'Nông sản hữu cơ đạt chuẩn tươi ngon được canh tác tự nhiên, thu hoạch tại vườn và đóng gói ngay trong ngày.'}</p>

          {/* AI Quality Card from Figma */}
          <div className="analysis-card">
            <div className="analysis-head">
              <div className="ai-orb">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <strong>Báo cáo Giám định AI (Vision)</strong>
                <small>Phân tích độ chín, khuyết tật bề mặt & màu sắc</small>
              </div>
              <div className="verified">
                <Shield className="w-3.5 h-3.5 text-[#176b45]" />
                <span>Verified</span>
              </div>
            </div>

            <div className="analysis-grade">
              <div>
                <small>TIÊU CHUẨN PHÂN HẠNG</small>
                <strong>{product.ai_quality || 'Hạng 1 (Grade 1)'}</strong>
                <span>Chất lượng xuất sắc · Đạt chuẩn an toàn</span>
              </div>
              <div className="confidence">
                <div>
                  <strong>{product.ai_confidence || 98.4}%</strong>
                  <small>ĐỘ TIN CẬY</small>
                </div>
              </div>
            </div>

            <div className="condition">
              <span>Tình trạng bề mặt</span>
              <strong>
                <Check className="w-4 h-4 text-[#176b45]" />{' '}
                {product.surface_condition || 'Mặt quả nhẵn, không có đốm nấm hay khuyết tật'}
              </strong>
            </div>

            <div className="condition">
              <span>Độ tươi & màu sắc</span>
              <strong>
                <Check className="w-4 h-4 text-[#176b45]" />{' '}
                {product.color_consistency || 'Sắc tố đồng đều 96%, độ tươi 5–7 ngày'}
              </strong>
            </div>
          </div>

          {/* Quantity Selector */}
          <div className="quantity">
            <span className="font-semibold text-[#53645b]">Số lượng mua</span>
            <div>
              <button
                type="button"
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
              >
                −
              </button>
              <strong>{quantity} {product.unit || 'kg'}</strong>
              <button
                type="button"
                onClick={() => setQuantity(quantity + 1)}
              >
                +
              </button>
            </div>
          </div>

          {/* Buy Actions */}
          <div className="buy-actions">
            <button
              type="button"
              className="button secondary"
              onClick={handleAddToCart}
            >
              <ShoppingBag className="w-4 h-4" /> Thêm vào giỏ
            </button>
            <button
              type="button"
              className="button primary"
              onClick={handleBuyNow}
            >
              Mua ngay <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Related Products / Khám phá thêm */}
      {relatedProducts && relatedProducts.length > 0 && (
        <div className="mt-16 pt-10 border-t border-[#dce5df]">
          <div className="section-row mb-6">
            <div>
              <div className="section-title text-xl font-bold">Nông sản cùng loại gợi ý</div>
              <p>Khám phá thêm các nông sản tươi ngon cùng danh mục, đạt chuẩn kiểm định AI</p>
            </div>
            <Link
              to={`/products?category=${encodeURIComponent(product.category || 'Rau củ')}`}
              className="text-button"
            >
              Xem thêm {product.category} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="product-grid">
            {relatedProducts.map((p) => (
              <article
                key={p.id}
                className="product-card cursor-pointer group"
                onClick={() => {
                  navigate(`/products/${p.id}`);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
              >
                <div className="product-photo relative">
                  <img src={p.image_url} alt={p.name} />
                  <div className="ai-badge">
                    <Sparkles className="w-3.5 h-3.5 text-[#176b45]" />
                    <span>AI Quality</span>
                    <strong>{p.ai_quality ? p.ai_quality.replace(/\(.*\)/, '').trim() : 'Loại 1'}</strong>
                  </div>
                  <button
                    type="button"
                    className="quick-add"
                    title="Thêm nhanh vào giỏ"
                    onClick={(e) => {
                      e.stopPropagation();
                      addToCart(p, 1);
                      toast.success(`Đã thêm ${p.name} vào giỏ hàng!`);
                    }}
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>

                <div className="product-info">
                  <small>{p.farm_name || 'Green Valley Farm'}</small>
                  <div className="product-name line-clamp-1">{p.name}</div>
                  <div className="product-bottom">
                    <strong>{Number(p.price).toLocaleString('vi-VN')} đ</strong>
                    <span>/ {p.unit || 'kg'}</span>
                    <div className="rating">★ {p.rating || '4.9'}</div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
