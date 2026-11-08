import { useState, useEffect, useMemo } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import {
  Search,
  Sparkles,
  Plus,
  Filter,
  Shield,
  X,
  SlidersHorizontal,
  Eye,
  ShoppingBag,
  Check,
  MapPin,
  RotateCcw,
  ArrowUpDown,
  ArrowRight,
  TrendingUp,
  Tag,
  Package,
} from 'lucide-react';
import { productsAPI } from '../services/api';
import { addToCart } from '../store/authStore';
import toast from 'react-hot-toast';

const initialSampleProducts = [
  {
    id: 'prod_001',
    name: 'Cà chua chín mọng Đà Lạt',
    farm_name: 'Green Valley Farm',
    description: 'Cà chua chín cây hữu cơ thu hoạch tại cao nguyên Đà Lạt. Vỏ căng mọng, vị ngọt thanh tự nhiên, giàu vitamin C và Lycopene.',
    price: 45000,
    unit: 'kg',
    category: 'Rau củ',
    origin: 'Đà Lạt, Lâm Đồng',
    image_url: 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 150,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.98,
    freshness_score: 98,
    rating: 4.9,
    sold_count: 320,
  },
  {
    id: 'prod_002',
    name: 'Giỏ nông sản hữu cơ tổng hợp',
    farm_name: 'Sunny Fields Co.',
    description: 'Hộp tuyển chọn gồm 5 loại rau củ tươi ngon thu hoạch trong ngày: cà chua, dưa leo, cà rốt baby, xà lách thủy canh, cải ngọt.',
    price: 185000,
    unit: 'giỏ (5kg)',
    category: 'Rau củ',
    origin: 'Đà Lạt, Lâm Đồng',
    image_url: 'https://images.unsplash.com/photo-1624668430039-0175a0fbf006?auto=format&fit=crop&w=1200&q=85',
    stock_quantity: 45,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.99,
    freshness_score: 99,
    rating: 5.0,
    sold_count: 412,
  },
  {
    id: 'prod_003',
    name: 'Cà rốt giòn ngọt Mộc Châu',
    farm_name: 'Mekong Roots',
    description: 'Cà rốt trồng trên đất đỏ bazan Mộc Châu, củ thon đều, giòn ngọt, giàu beta-carotene, thích hợp ép nước hoặc nấu súp.',
    price: 32000,
    unit: 'kg',
    category: 'Rau củ',
    origin: 'Mộc Châu, Sơn La',
    image_url: 'https://images.unsplash.com/photo-1609842947419-ba4f04d5d60f?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 85,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.96,
    freshness_score: 96,
    rating: 4.8,
    sold_count: 290,
  },
  {
    id: 'prod_004',
    name: 'Cam sành Hàm Yên mọng nước',
    farm_name: 'Tuyên Quang Organic',
    description: 'Cam sành đặc sản vùng núi Hàm Yên - Tuyên Quang, vị ngọt thanh mát, tép cam vàng ươm mọng nước, nhiều vitamin tự nhiên.',
    price: 55000,
    unit: 'kg',
    category: 'Trái cây',
    origin: 'Hàm Yên, Tuyên Quang',
    image_url: 'https://images.unsplash.com/photo-1582979512210-99b6a53386f9?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 120,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.97,
    freshness_score: 97,
    rating: 4.9,
    sold_count: 530,
  },
  {
    id: 'prod_005',
    name: 'Bơ sáp 034 Tây Nguyên',
    farm_name: 'Lâm Đồng Farms',
    description: 'Bơ 034 quả dài, cơm vàng dẻo quánh, hạt bé xíu, béo ngậy thơm ngon nức tiếng xứ trà Bảo Lộc.',
    price: 75000,
    unit: 'kg',
    category: 'Trái cây',
    origin: 'Bảo Lộc, Lâm Đồng',
    image_url: 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 60,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.98,
    freshness_score: 98,
    rating: 4.9,
    sold_count: 340,
  },
  {
    id: 'prod_006',
    name: 'Dâu tây giống Nhật Hana Mộc Châu',
    farm_name: 'Mộc Châu Berry Garden',
    description: 'Dâu tây Hana quả đỏ mọng, vị ngọt lịm thơm ngát, trồng chuẩn nhà kính hữu cơ tại cao nguyên sương mù Mộc Châu.',
    price: 135000,
    unit: 'hộp (500g)',
    category: 'Trái cây',
    origin: 'Mộc Châu, Sơn La',
    image_url: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 30,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.99,
    freshness_score: 99,
    rating: 5.0,
    sold_count: 680,
  },
  {
    id: 'prod_007',
    name: 'Bưởi da xanh ruột hồng Bến Tre',
    farm_name: 'Bến Tre Green Fruit',
    description: 'Bưởi da xanh đặc sản miền Tây, tép bưởi hồng mọng nước, vị ngọt thanh không hạt, bổ sung khoáng chất tự nhiên.',
    price: 85000,
    unit: 'quả (~1.4kg)',
    category: 'Trái cây',
    origin: 'Bến Tre',
    image_url: 'https://images.unsplash.com/photo-1577234286642-fc512a5f8f11?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 70,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.96,
    freshness_score: 96,
    rating: 4.8,
    sold_count: 215,
  },
  {
    id: 'prod_008',
    name: 'Xà lách thủy canh Romaine',
    farm_name: 'Eco Hydroponics Farm',
    description: 'Xà lách Romaine giòn ngọt, trồng trong nhà kính công nghệ cao, rửa sạch ăn liền cực kỳ tiện lợi cho món salad tươi.',
    price: 28000,
    unit: 'túi (300g)',
    category: 'Rau củ',
    origin: 'Đà Lạt, Lâm Đồng',
    image_url: 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 90,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.97,
    freshness_score: 97,
    rating: 4.7,
    sold_count: 180,
  },
  {
    id: 'prod_009',
    name: 'Dưa leo baby giòn ngọt',
    farm_name: 'Vĩnh Long Eco Farm',
    description: 'Dưa leo mini giống Hà Lan, vỏ mỏng ruột đặc, giòn rụm không đắng, ăn trực tiếp hoặc làm nộm chua ngọt.',
    price: 30000,
    unit: 'kg',
    category: 'Rau củ',
    origin: 'Vĩnh Long',
    image_url: 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 8,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.95,
    freshness_score: 95,
    rating: 4.8,
    sold_count: 310,
  },
  {
    id: 'prod_010',
    name: 'Cải xoăn Kale xoăn hữu cơ',
    farm_name: 'Dalat Organics',
    description: 'Nữ hoàng của các loại rau xanh - giàu chất chống oxy hóa, canxi và sắt, thích hợp làm sinh tố detox hoặc salad.',
    price: 48000,
    unit: 'bó (400g)',
    category: 'Rau củ',
    origin: 'Đà Lạt, Lâm Đồng',
    image_url: 'https://images.unsplash.com/photo-1524179091875-bf99a9a6af57?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 55,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.99,
    freshness_score: 99,
    rating: 4.9,
    sold_count: 275,
  },
  {
    id: 'prod_013',
    name: 'Nấm đùi gà tươi hữu cơ',
    farm_name: 'Viet Mushroom Co.',
    description: 'Nấm đùi gà thân mập mạp, thịt nấm trắng tinh, thơm mùi hạnh nhân, xào hoặc nướng ăn giòn ngọt như thịt gà.',
    price: 45000,
    unit: 'gói (300g)',
    category: 'Nấm ăn',
    origin: 'Vĩnh Phúc',
    image_url: 'https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 50,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.97,
    freshness_score: 97,
    rating: 4.9,
    sold_count: 220,
  },
  {
    id: 'prod_015',
    name: 'Tỏi cô đơn Lý Sơn chính hiệu',
    farm_name: 'Lý Sơn Island Heritage',
    description: 'Đặc sản nức tiếng đảo Lý Sơn, củ tỏi tròn 1 nhánh duy nhất, vị cay nồng thơm dịu, dược tính cao gấp 5 lần tỏi thường.',
    price: 220000,
    unit: 'kg',
    category: 'Gia vị',
    origin: 'Lý Sơn, Quảng Ngãi',
    image_url: 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 25,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.99,
    freshness_score: 99,
    rating: 5.0,
    sold_count: 480,
  },
  {
    id: 'prod_017',
    name: 'Gạo ST25 Ông Cua (Gạo ngon nhất thế giới)',
    farm_name: 'Sóc Trăng Rice Delta',
    description: 'Gạo tiến vua hạt dài trong vắt, cơm chín dẻo mềm, thơm ngát mùi lá dứa tự nhiên, để nguội vẫn giữ độ dẻo thơm tuyệt hảo.',
    price: 175000,
    unit: 'túi (5kg)',
    category: 'Gạo & Ngũ cốc',
    origin: 'Sóc Trăng',
    image_url: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 110,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.99,
    freshness_score: 99,
    rating: 5.0,
    sold_count: 890,
  },
  {
    id: 'prod_018',
    name: 'Hạt điều rang củi lụa Bình Phước',
    farm_name: 'Bình Phước Agro',
    description: 'Hạt điều loại A hạt to tròn đều, rang củi thủ công giữ trọn độ ngậy béo tự nhiên, vị muối thoang thoảng giòn tan.',
    price: 140000,
    unit: 'hộp (500g)',
    category: 'Thực phẩm khô',
    origin: 'Bình Phước',
    image_url: 'https://images.unsplash.com/photo-1509912760195-4f3b5eb5b210?auto=format&fit=crop&w=900&q=85',
    stock_quantity: 40,
    ai_quality: 'Loại 1 (Xuất sắc)',
    ai_confidence: 0.98,
    freshness_score: 98,
    rating: 4.9,
    sold_count: 420,
  },
];

const categoryIcons = {
  All: '🌿',
  'Tất cả': '🌿',
  'Rau củ': '🍅',
  'Trái cây': '🍊',
  'Nấm ăn': '🍄',
  'Gia vị': '🧄',
  'Gạo & Ngũ cốc': '🌾',
  'Thực phẩm khô': '🥜',
};

const priceRanges = [
  { label: 'Tất cả mức giá', min: null, max: null },
  { label: 'Dưới 40.000 đ', min: 0, max: 40000 },
  { label: '40.000 đ – 80.000 đ', min: 40000, max: 80000 },
  { label: '80.000 đ – 150.000 đ', min: 80000, max: 150000 },
  { label: 'Trên 150.000 đ', min: 150000, max: null },
];

const sortOptions = [
  { value: 'popular', label: 'Bán chạy nhất' },
  { value: 'rating_desc', label: 'Đánh giá cao nhất' },
  { value: 'price_asc', label: 'Giá: Thấp đến cao' },
  { value: 'price_desc', label: 'Giá: Cao đến thấp' },
  { value: 'newest', label: 'Mới thu hoạch' },
];

export default function Products() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // Read initial values from URL query parameters
  const initialCategory = searchParams.get('category') || 'All';
  const initialSearch = searchParams.get('search') || '';
  const initialSort = searchParams.get('sort') || 'popular';

  const [products, setProducts] = useState(initialSampleProducts);
  const [categories, setCategories] = useState(['All', 'Rau củ', 'Trái cây', 'Nấm ăn', 'Gia vị', 'Gạo & Ngũ cốc', 'Thực phẩm khô']);
  const [origins, setOrigins] = useState([]);
  const [popularTags, setPopularTags] = useState([
    'Cà chua Đà Lạt',
    'Bơ sáp 034',
    'Cam sành',
    'Dâu tây Hana',
    'Gạo ST25',
    'Nấm tươi',
    'Rau hữu cơ',
    'Tỏi Lý Sơn',
  ]);

  const [selectedCategory, setSelectedCategory] = useState(initialCategory);
  const [searchInput, setSearchInput] = useState(initialSearch);
  const [activeSearch, setActiveSearch] = useState(initialSearch);
  const [sortBy, setSortBy] = useState(initialSort);
  const [selectedPriceRangeIndex, setSelectedPriceRangeIndex] = useState(0);
  const [selectedAIQuality, setSelectedAIQuality] = useState('All');
  const [selectedOrigin, setSelectedOrigin] = useState('All');
  const [inStockOnly, setInStockOnly] = useState(false);
  const [showFilterDrawer, setShowFilterDrawer] = useState(false);
  const [loading, setLoading] = useState(false);

  // Quick View Modal State
  const [quickViewProduct, setQuickViewProduct] = useState(null);
  const [quickViewQty, setQuickViewQty] = useState(1);

  // Synchronize when URL searchParams change externally (e.g. Back button or Home search)
  useEffect(() => {
    const cat = searchParams.get('category') || 'All';
    const s = searchParams.get('search') || '';
    const sort = searchParams.get('sort') || 'popular';
    setSelectedCategory(cat);
    setSearchInput(s);
    setActiveSearch(s);
    setSortBy(sort);
  }, [searchParams]);

  // Fetch metadata: Categories, Origins, Tags
  useEffect(() => {
    productsAPI.getCategories()
      .then((res) => {
        if (res.data?.categories) {
          setCategories(['All', ...res.data.categories.filter((c) => c !== 'All')]);
        }
      })
      .catch((err) => console.warn('Could not fetch categories:', err));

    productsAPI.getOrigins()
      .then((res) => {
        if (res.data?.origins) setOrigins(res.data.origins);
      })
      .catch((err) => console.warn('Could not fetch origins:', err));

    productsAPI.getTags()
      .then((res) => {
        if (res.data?.tags) setPopularTags(res.data.tags);
      })
      .catch((err) => console.warn('Could not fetch tags:', err));
  }, []);

  // Fetch products from backend
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const priceFilter = priceRanges[selectedPriceRangeIndex];
      const params = {
        category: selectedCategory === 'All' ? undefined : selectedCategory,
        search: activeSearch.trim() || undefined,
        sort_by: sortBy,
        min_price: priceFilter?.min ?? undefined,
        max_price: priceFilter?.max ?? undefined,
        ai_quality: selectedAIQuality === 'All' ? undefined : selectedAIQuality,
        origin: selectedOrigin === 'All' ? undefined : selectedOrigin,
        in_stock: inStockOnly || undefined,
        per_page: 50,
      };

      const res = await productsAPI.getAll(params);
      if (res.data?.items) {
        setProducts(res.data.items);
      }
    } catch (err) {
      console.warn('API error, falling back to local dataset filtering:', err);
      // Fallback local filtering
      const filtered = initialSampleProducts.filter((p) => {
        if (selectedCategory !== 'All' && !p.category?.toLowerCase().includes(selectedCategory.toLowerCase())) {
          return false;
        }
        if (activeSearch.trim()) {
          const q = activeSearch.toLowerCase();
          const match =
            p.name.toLowerCase().includes(q) ||
            p.farm_name?.toLowerCase().includes(q) ||
            p.origin?.toLowerCase().includes(q);
          if (!match) return false;
        }
        return true;
      });
      setProducts(filtered);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [
    selectedCategory,
    activeSearch,
    sortBy,
    selectedPriceRangeIndex,
    selectedAIQuality,
    selectedOrigin,
    inStockOnly,
  ]);

  // Update URL params
  const updateUrlParams = (newCat, newSearch, newSort) => {
    const params = new URLSearchParams();
    if (newCat && newCat !== 'All') params.set('category', newCat);
    if (newSearch && newSearch.trim()) params.set('search', newSearch.trim());
    if (newSort && newSort !== 'popular') params.set('sort', newSort);
    setSearchParams(params, { replace: true });
  };

  const handleCategorySelect = (cat) => {
    setSelectedCategory(cat);
    updateUrlParams(cat, activeSearch, sortBy);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setActiveSearch(searchInput);
    updateUrlParams(selectedCategory, searchInput, sortBy);
  };

  const handleClearSearch = () => {
    setSearchInput('');
    setActiveSearch('');
    updateUrlParams(selectedCategory, '', sortBy);
  };

  const handleTagClick = (tag) => {
    const cleanTag = tag.replace(/^[^\w\s\u00C0-\u1EF9]+/u, '').trim();
    setSearchInput(cleanTag);
    setActiveSearch(cleanTag);
    updateUrlParams(selectedCategory, cleanTag, sortBy);
  };

  const handleResetFilters = () => {
    setSelectedCategory('All');
    setSearchInput('');
    setActiveSearch('');
    setSortBy('popular');
    setSelectedPriceRangeIndex(0);
    setSelectedAIQuality('All');
    setSelectedOrigin('All');
    setInStockOnly(false);
    setSearchParams({}, { replace: true });
  };

  const handleQuickAdd = (e, product) => {
    e.stopPropagation();
    addToCart(product, 1);
    toast.success(`Đã thêm 1 ${product.unit || 'kg'} ${product.name} vào giỏ hàng!`, {
      icon: '🛒',
    });
  };

  const openQuickView = (e, product) => {
    e.stopPropagation();
    setQuickViewProduct(product);
    setQuickViewQty(1);
  };

  const handleModalAddToCart = () => {
    if (!quickViewProduct) return;
    addToCart(quickViewProduct, quickViewQty);
    toast.success(`Đã thêm ${quickViewQty} ${quickViewProduct.unit || 'kg'} ${quickViewProduct.name} vào giỏ hàng!`, {
      icon: '🌿',
    });
    setQuickViewProduct(null);
  };

  const handleModalBuyNow = () => {
    if (!quickViewProduct) return;
    addToCart(quickViewProduct, quickViewQty);
    setQuickViewProduct(null);
    navigate('/cart');
  };

  // Count active non-default filters
  const activeFilterCount = useMemo(() => {
    let count = 0;
    if (selectedCategory !== 'All') count++;
    if (activeSearch.trim()) count++;
    if (selectedPriceRangeIndex !== 0) count++;
    if (selectedAIQuality !== 'All') count++;
    if (selectedOrigin !== 'All') count++;
    if (inStockOnly) count++;
    return count;
  }, [
    selectedCategory,
    activeSearch,
    selectedPriceRangeIndex,
    selectedAIQuality,
    selectedOrigin,
    inStockOnly,
  ]);

  return (
    <div className="content">
      {/* Page Heading & Stats */}
      <div className="page-heading flex-wrap gap-4">
        <div>
          <div className="eyebrow flex items-center gap-1.5 font-bold tracking-wider">
            <Sparkles className="w-4 h-4 text-[#176b45]" />
            <span>MARKETPLACE / SÀN NÔNG SẢN SẠCH</span>
          </div>
          <h1 className="title text-2xl md:text-3xl text-[#183229]">
            Khám phá & Lựa chọn Nông sản
          </h1>
          <p className="text-sm text-[#718078] mt-1">
            Nông sản tươi sạch từ các nhà vườn Việt Nam, 100% kiểm định chất lượng minh bạch bởi AI Vision
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="date-pill font-semibold text-xs flex items-center gap-1.5 bg-white shadow-sm border border-[#dce5df] px-3.5 py-2 rounded-xl text-[#183229]">
            <Package className="w-4 h-4 text-[#176b45]" />
            <span>
              {loading ? 'Đang cập nhật...' : `${products.length} sản phẩm sẵn sàng`}
            </span>
          </div>

          <button
            onClick={() => setShowFilterDrawer(!showFilterDrawer)}
            className={`button px-3.5 py-2 rounded-xl text-xs font-bold transition-all border ${
              showFilterDrawer || activeFilterCount > 0
                ? 'bg-[#176b45] text-white border-[#176b45] shadow-sm'
                : 'bg-white text-[#53655d] border-[#dce5df] hover:border-[#176b45]'
            }`}
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>Bộ lọc nâng cao</span>
            {activeFilterCount > 0 && (
              <span className="w-4 h-4 rounded-full bg-[#ef8b45] text-white text-[10px] font-bold flex items-center justify-center">
                {activeFilterCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Main Search Bar & Quick Tags */}
      <div className="bg-white border border-[#dce5df] rounded-2xl p-5 mb-6 shadow-sm">
        {/* Search Input Row */}
        <form onSubmit={handleSearchSubmit} className="relative flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-[#88958e] absolute left-4 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm kiếm theo tên nông sản, nhà vườn (Green Valley...), vùng miền (Đà Lạt, Mộc Châu...)"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              className="w-full pl-12 pr-10 py-3.5 text-sm bg-[#f6f8f4] border border-[#dce5df] rounded-xl focus:bg-white focus:border-[#176b45] focus:outline-none focus:ring-2 focus:ring-[#176b45]/15 transition-all text-[#183229] font-medium"
            />
            {searchInput && (
              <button
                type="button"
                onClick={handleClearSearch}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#88958e] hover:text-[#183229] p-1"
                title="Xóa tìm kiếm"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <button
            type="submit"
            className="button bg-[#176b45] hover:bg-[#115a39] text-white px-6 py-3.5 rounded-xl font-bold text-sm shadow-sm transition-all"
          >
            Tìm kiếm
          </button>
        </form>

        {/* Popular Tags */}
        <div className="flex items-center gap-2 flex-wrap mt-3.5 pt-3 border-t border-[#edf2ee]">
          <div className="flex items-center gap-1 text-[11px] font-bold text-[#88958e] uppercase tracking-wider mr-1">
            <Tag className="w-3.5 h-3.5 text-[#176b45]" />
            <span>Gợi ý:</span>
          </div>
          {popularTags.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => handleTagClick(tag)}
              className="text-xs bg-[#f4f7f4] hover:bg-[#e6efe8] text-[#344b41] hover:text-[#176b45] font-semibold px-3 py-1.5 rounded-lg transition-colors border border-[#e2eae4]"
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Category Tabs & Sort Toolbar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
        {/* Category Chips with Icons */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 max-w-full scrollbar-none">
          {categories.map((cat) => {
            const isActive = selectedCategory === cat;
            const icon = categoryIcons[cat] || '🌱';
            return (
              <button
                key={cat}
                onClick={() => handleCategorySelect(cat)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap border ${
                  isActive
                    ? 'bg-[#176b45] text-white border-[#176b45] shadow-sm transform -translate-y-0.5'
                    : 'bg-white text-[#52635a] border-[#dce5df] hover:border-[#176b45] hover:text-[#176b45]'
                }`}
              >
                <span>{icon}</span>
                <span>{cat === 'All' ? 'Tất cả nông sản' : cat}</span>
              </button>
            );
          })}
        </div>

        {/* Sorting Dropdown */}
        <div className="flex items-center gap-3 self-end lg:self-auto shrink-0">
          <div className="flex items-center gap-1.5 text-xs text-[#718078] font-bold">
            <ArrowUpDown className="w-3.5 h-3.5 text-[#176b45]" />
            <span>Sắp xếp:</span>
          </div>
          <select
            value={sortBy}
            onChange={(e) => {
              setSortBy(e.target.value);
              updateUrlParams(selectedCategory, activeSearch, e.target.value);
            }}
            className="bg-white border border-[#dce5df] text-[#183229] font-bold text-xs rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-[#176b45] cursor-pointer shadow-sm"
          >
            {sortOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Advanced Filter Drawer (Collapsible) */}
      {showFilterDrawer && (
        <div className="bg-white border border-[#dce5df] rounded-2xl p-5 mb-8 shadow-sm animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-3.5 border-b border-[#edf2ee] mb-4">
            <div className="flex items-center gap-2 font-bold text-sm text-[#183229]">
              <Filter className="w-4 h-4 text-[#176b45]" />
              <span>Tùy chỉnh Bộ lọc Nông sản</span>
            </div>
            {activeFilterCount > 0 && (
              <button
                type="button"
                onClick={handleResetFilters}
                className="text-xs font-bold text-[#ef8b45] hover:text-[#d7722d] flex items-center gap-1.5 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Xóa toàn bộ lọc ({activeFilterCount})</span>
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Price Range Filter */}
            <div>
              <div className="text-xs font-bold uppercase text-[#88958e] tracking-wider mb-2.5">
                Khoảng giá (VNĐ)
              </div>
              <div className="flex flex-col gap-1.5">
                {priceRanges.map((pr, idx) => (
                  <label
                    key={pr.label}
                    className="flex items-center gap-2.5 text-xs text-[#35483f] font-medium cursor-pointer hover:text-[#176b45]"
                  >
                    <input
                      type="radio"
                      name="priceRange"
                      checked={selectedPriceRangeIndex === idx}
                      onChange={() => setSelectedPriceRangeIndex(idx)}
                      className="accent-[#176b45] w-3.5 h-3.5"
                    />
                    <span>{pr.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* AI Quality Grade Filter */}
            <div>
              <div className="text-xs font-bold uppercase text-[#88958e] tracking-wider mb-2.5 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-[#176b45]" />
                <span>Kiểm định AI Quality</span>
              </div>
              <div className="flex flex-col gap-1.5">
                {[
                  { value: 'All', label: 'Tất cả phân hạng' },
                  { value: 'Loại 1', label: 'Hạng 1 (Grade 1 - Xuất sắc)' },
                  { value: 'Loại 2', label: 'Hạng 2 (Grade 2 - Đạt chuẩn)' },
                ].map((q) => (
                  <label
                    key={q.value}
                    className="flex items-center gap-2.5 text-xs text-[#35483f] font-medium cursor-pointer hover:text-[#176b45]"
                  >
                    <input
                      type="radio"
                      name="aiQuality"
                      checked={selectedAIQuality === q.value}
                      onChange={() => setSelectedAIQuality(q.value)}
                      className="accent-[#176b45] w-3.5 h-3.5"
                    />
                    <span>{q.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Origin & Availability */}
            <div>
              <div className="text-xs font-bold uppercase text-[#88958e] tracking-wider mb-2.5 flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-[#176b45]" />
                <span>Vùng miền / Xuất xứ</span>
              </div>
              <select
                value={selectedOrigin}
                onChange={(e) => setSelectedOrigin(e.target.value)}
                className="w-full bg-[#f6f8f4] border border-[#dce5df] text-[#183229] font-medium text-xs rounded-xl p-2.5 mb-4 focus:outline-none focus:border-[#176b45]"
              >
                <option value="All">Tất cả vùng miền</option>
                {origins.map((orig) => (
                  <option key={orig} value={orig}>
                    {orig}
                  </option>
                ))}
              </select>

              <label className="flex items-center gap-2 text-xs font-bold text-[#183229] cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={inStockOnly}
                  onChange={(e) => setInStockOnly(e.target.checked)}
                  className="accent-[#176b45] w-4 h-4 rounded"
                />
                <span>Chỉ hiển thị sản phẩm còn hàng</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Applied Filters Tags Pill (if any) */}
      {activeFilterCount > 0 && (
        <div className="flex items-center gap-2 flex-wrap mb-6">
          <span className="text-xs font-bold text-[#718078]">Đang lọc:</span>
          {selectedCategory !== 'All' && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              Danh mục: {selectedCategory}
              <X className="w-3 h-3 cursor-pointer" onClick={() => handleCategorySelect('All')} />
            </span>
          )}
          {activeSearch && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              Từ khóa: "{activeSearch}"
              <X className="w-3 h-3 cursor-pointer" onClick={handleClearSearch} />
            </span>
          )}
          {selectedPriceRangeIndex !== 0 && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              Giá: {priceRanges[selectedPriceRangeIndex]?.label}
              <X className="w-3 h-3 cursor-pointer" onClick={() => setSelectedPriceRangeIndex(0)} />
            </span>
          )}
          {selectedAIQuality !== 'All' && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              AI: {selectedAIQuality}
              <X className="w-3 h-3 cursor-pointer" onClick={() => setSelectedAIQuality('All')} />
            </span>
          )}
          {selectedOrigin !== 'All' && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              Xuất xứ: {selectedOrigin}
              <X className="w-3 h-3 cursor-pointer" onClick={() => setSelectedOrigin('All')} />
            </span>
          )}
          {inStockOnly && (
            <span className="inline-flex items-center gap-1 bg-[#edf7f1] text-[#176b45] text-xs font-bold px-3 py-1 rounded-full border border-[#c4e6d2]">
              Chỉ còn hàng
              <X className="w-3 h-3 cursor-pointer" onClick={() => setInStockOnly(false)} />
            </span>
          )}
          <button
            onClick={handleResetFilters}
            className="text-xs font-bold text-red-600 hover:underline ml-1"
          >
            Xóa tất cả
          </button>
        </div>
      )}

      {/* Product Grid / Loader / Empty State */}
      {loading ? (
        <div className="py-24 text-center">
          <div className="w-11 h-11 border-4 border-[#176b45] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm font-semibold text-[#718078]">Đang tải danh sách nông sản & kết quả kiểm định AI...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="table-card p-16 text-center rounded-2xl bg-white border border-[#dce5df]">
          <div className="w-16 h-16 rounded-2xl bg-[#f0f6f2] text-[#176b45] flex items-center justify-center mx-auto mb-4">
            <Search className="w-8 h-8" />
          </div>
          <h3 className="font-extrabold text-lg text-[#183229] mb-1">
            Không tìm thấy nông sản phù hợp
          </h3>
          <p className="text-[#718078] text-sm max-w-md mx-auto mb-6">
            Rất tiếc, không có nông sản nào khớp với từ khóa "{activeSearch}" hoặc tiêu chuẩn lọc hiện tại. Bạn có thể thử tìm kiếm từ khóa khác hoặc xóa bộ lọc.
          </p>
          <div className="flex items-center justify-center gap-3">
            <button
              onClick={handleResetFilters}
              className="button bg-[#176b45] hover:bg-[#115a39] text-white px-5 py-2.5 rounded-xl font-bold text-xs shadow-sm transition-all"
            >
              Xem tất cả nông sản
            </button>
          </div>
        </div>
      ) : (
        <div className="product-grid">
          {products.map((p) => {
            const isLowStock = p.stock_quantity !== undefined && p.stock_quantity <= 10 && p.stock_quantity > 0;
            const isOutOfStock = p.stock_quantity !== undefined && p.stock_quantity === 0;

            return (
              <article
                key={p.id}
                className="product-card group relative"
                onClick={() => navigate(`/products/${p.id}`)}
              >
                {/* Product Photo & Floating Badges */}
                <div className="product-photo relative">
                  <img
                    src={p.image_url || 'https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85'}
                    alt={p.name}
                    loading="lazy"
                  />

                  {/* AI Quality Badge */}
                  <div className="ai-badge">
                    <Sparkles className="w-3.5 h-3.5 text-[#176b45]" />
                    <span>AI Quality</span>
                    <strong>{p.ai_quality ? p.ai_quality.replace(/\(.*\)/, '').trim() : 'Hạng 1'}</strong>
                  </div>

                  {/* Quick View Button on Hover */}
                  <button
                    type="button"
                    onClick={(e) => openQuickView(e, p)}
                    className="absolute left-2.5 bottom-2.5 bg-white/90 hover:bg-white text-[#183229] p-2 rounded-lg text-xs font-bold shadow-md opacity-0 group-hover:opacity-100 transition-all flex items-center gap-1.5 backdrop-blur-sm"
                    title="Xem nhanh thông tin AI & Nông trại"
                  >
                    <Eye className="w-3.5 h-3.5 text-[#176b45]" />
                    <span>Xem nhanh</span>
                  </button>

                  {/* Quick Add To Cart Button */}
                  <button
                    type="button"
                    className="quick-add"
                    title="Thêm nhanh vào giỏ hàng"
                    disabled={isOutOfStock}
                    onClick={(e) => handleQuickAdd(e, p)}
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>

                {/* Product Info */}
                <div className="product-info">
                  <div className="flex items-center justify-between text-[11px] text-[#718078] mb-1">
                    <span className="font-semibold truncate max-w-[150px]">
                      {p.farm_name || p.farm || 'Green Valley Farm'}
                    </span>
                    {p.origin && (
                      <span className="flex items-center gap-0.5 text-[10px] text-[#84958d]">
                        <MapPin className="w-2.5 h-2.5 text-[#176b45]" />
                        <span className="truncate max-w-[100px]">{p.origin.split(',')[0]}</span>
                      </span>
                    )}
                  </div>

                  <h3 className="product-name line-clamp-2" title={p.name}>
                    {p.name}
                  </h3>

                  {/* Stock status indicator */}
                  <div className="mb-2">
                    {isOutOfStock ? (
                      <span className="text-[10px] font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded">
                        Tạm hết hàng
                      </span>
                    ) : isLowStock ? (
                      <span className="text-[10px] font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded">
                        Sắp hết: còn {p.stock_quantity} {p.unit || 'kg'}
                      </span>
                    ) : (
                      <span className="text-[10px] font-medium text-[#176b45] bg-[#edf7f1] px-2 py-0.5 rounded">
                        ✓ Tươi mới hôm nay
                      </span>
                    )}
                  </div>

                  {/* Price & Rating */}
                  <div className="product-bottom">
                    <strong>{Number(p.price).toLocaleString('vi-VN')} đ</strong>
                    <span>/ {p.unit || 'kg'}</span>
                    <div className="rating">★ {p.rating || '4.9'}</div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}

      {/* QUICK VIEW MODAL (Xem nhanh & Lựa chọn) */}
      {quickViewProduct && (
        <div
          className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in"
          onClick={() => setQuickViewProduct(null)}
        >
          <div
            className="bg-white rounded-2xl max-w-2xl w-full overflow-hidden shadow-2xl relative border border-[#dce5df] animate-in zoom-in-95 duration-200"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close button */}
            <button
              onClick={() => setQuickViewProduct(null)}
              className="absolute right-4 top-4 z-10 w-8 h-8 rounded-full bg-white/80 hover:bg-white text-[#183229] flex items-center justify-center shadow-md transition-all"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="grid grid-cols-1 md:grid-cols-2">
              {/* Product Photo in Modal */}
              <div className="relative h-64 md:h-full min-h-[300px] bg-[#f0f4f1]">
                <img
                  src={quickViewProduct.image_url}
                  alt={quickViewProduct.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute left-4 top-4 ai-badge large bg-white/95 shadow-md">
                  <Sparkles className="w-4 h-4 text-[#176b45]" />
                  <span>AI Inspected · {quickViewProduct.ai_quality || 'Loại 1'}</span>
                </div>
              </div>

              {/* Product Details & Selection Actions */}
              <div className="p-6 flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-1.5 text-xs text-[#718078] font-bold uppercase tracking-wider mb-1">
                    <span>{quickViewProduct.category}</span>
                    <span>·</span>
                    <span className="text-[#176b45]">{quickViewProduct.farm_name || 'Nông trại Việt'}</span>
                  </div>

                  <h2 className="text-xl font-extrabold text-[#183229] mb-2 leading-tight">
                    {quickViewProduct.name}
                  </h2>

                  <div className="flex items-center gap-3 text-xs mb-3 text-[#718078]">
                    <span className="text-[#ba6c32] font-bold">★ {quickViewProduct.rating || '4.9'}</span>
                    <span>·</span>
                    <span>Đã bán {quickViewProduct.sold_count || 120}</span>
                    <span>·</span>
                    <span className="flex items-center gap-0.5">
                      <MapPin className="w-3 h-3 text-[#176b45]" />
                      {quickViewProduct.origin || 'Việt Nam'}
                    </span>
                  </div>

                  <div className="text-2xl font-black text-[#176b45] mb-3 font-mono">
                    {Number(quickViewProduct.price).toLocaleString('vi-VN')} đ{' '}
                    <span className="text-xs font-semibold text-[#718078]">/ {quickViewProduct.unit || 'kg'}</span>
                  </div>

                  <p className="text-xs text-[#52645c] line-clamp-3 mb-4 leading-relaxed">
                    {quickViewProduct.description || 'Nông sản hữu cơ tươi ngon canh tác tự nhiên, thu hoạch tại vườn và đóng gói bảo quản đạt chuẩn.'}
                  </p>

                  {/* AI Vision Highlight Card */}
                  <div className="bg-[#f2f8f4] border border-[#cbe4d5] rounded-xl p-3 mb-4 text-xs">
                    <div className="flex items-center gap-1.5 font-bold text-[#176b45] mb-1">
                      <Shield className="w-3.5 h-3.5" />
                      <span>Kết quả Giám định AI (Vision)</span>
                    </div>
                    <div className="text-[11px] text-[#445b50]">
                      {quickViewProduct.ai_details || 'Đạt chuẩn VietGAP, ngoại quan đồng đều, độ tươi mới 96%.'}
                    </div>
                  </div>
                </div>

                {/* Quantity and Action Buttons */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-bold text-[#183229]">Số lượng mua:</span>
                    <div className="flex items-center border border-[#dce5df] rounded-lg overflow-hidden bg-white">
                      <button
                        type="button"
                        onClick={() => setQuickViewQty(Math.max(1, quickViewQty - 1))}
                        className="px-3 py-1 bg-[#f6f8f4] hover:bg-[#e9efe7] font-bold text-sm text-[#183229] transition-colors"
                      >
                        −
                      </button>
                      <span className="px-3 py-1 text-xs font-bold min-w-[48px] text-center text-[#183229]">
                        {quickViewQty} {quickViewProduct.unit || 'kg'}
                      </span>
                      <button
                        type="button"
                        onClick={() => setQuickViewQty(quickViewQty + 1)}
                        className="px-3 py-1 bg-[#f6f8f4] hover:bg-[#e9efe7] font-bold text-sm text-[#183229] transition-colors"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 mb-2.5">
                    <button
                      type="button"
                      onClick={handleModalAddToCart}
                      className="button bg-white border border-[#176b45] text-[#176b45] hover:bg-[#edf7f1] py-2.5 rounded-xl font-bold text-xs shadow-sm"
                    >
                      <ShoppingBag className="w-3.5 h-3.5" />
                      <span>Thêm vào giỏ</span>
                    </button>
                    <button
                      type="button"
                      onClick={handleModalBuyNow}
                      className="button bg-[#176b45] hover:bg-[#115a39] text-white py-2.5 rounded-xl font-bold text-xs shadow-sm"
                    >
                      <span>Mua ngay</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <Link
                    to={`/products/${quickViewProduct.id}`}
                    onClick={() => setQuickViewProduct(null)}
                    className="block text-center text-[11px] font-bold text-[#718078] hover:text-[#176b45] transition-colors"
                  >
                    Xem chi tiết nông sản & chứng nhận đầy đủ →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
