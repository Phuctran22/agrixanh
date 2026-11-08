import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: đính kèm JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('agrixanh_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor: xử lý lỗi 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('agrixanh_token');
      localStorage.removeItem('agrixanh_user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

// ===== AUTH =====
export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/profile', data),
  getAllUsers: (params) => api.get('/auth/users', { params }),
  toggleUserStatus: (userId, isActive) =>
    api.patch(`/auth/users/${userId}/status`, null, { params: { is_active: isActive } }),
  changeUserRole: (userId, newRole) =>
    api.patch(`/auth/users/${userId}/role`, null, { params: { new_role: newRole } }),
};

// ===== PRODUCTS =====
export const productsAPI = {
  getAll: (params) => api.get('/products', { params }),
  getById: (id) => api.get(`/products/${id}`),
  getCategories: () => api.get('/products/categories'),
  getOrigins: () => api.get('/products/origins'),
  getTags: () => api.get('/products/tags'),
  getFeatured: (limit = 4) => api.get('/products/featured', { params: { limit } }),
  getRelated: (id, limit = 4) => api.get(`/products/${id}/related`, { params: { limit } }),
  addCategory: (name) => api.post('/products/categories', { name }),
  deleteCategory: (name) => api.delete(`/products/categories/${name}`),
  create: (data) => api.post('/products', data),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`),
};

// ===== ORDERS =====
export const ordersAPI = {
  getAll: (params) => api.get('/orders', { params }),
  getById: (id) => api.get(`/orders/${id}`),
  create: (data) => api.post('/orders', data),
  preview: (data) => api.post('/orders/preview', data),
  updateStatus: (id, status) => api.patch(`/orders/${id}/status`, null, { params: { new_status: status } }),
  cancel: (id) => api.post(`/orders/${id}/cancel`),
};

// ===== INVENTORY =====
export const inventoryAPI = {
  getAll: () => api.get('/inventory'),
  getLowStock: () => api.get('/inventory/low-stock'),
  getExpiring: () => api.get('/inventory/expiring'),
  updateStock: (productId, quantity) =>
    api.patch(`/inventory/${productId}/stock`, null, { params: { quantity } }),
};

// ===== PAYMENTS =====
export const paymentsAPI = {
  getAll: () => api.get('/payments'),
  create: (data) => api.post('/payments', data),
  confirm: (id) => api.patch(`/payments/${id}/confirm`),
};

// ===== AI =====
export const aiAPI = {
  analyzeImage: (formData) =>
    api.post('/ai/analyze', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  analyzeUrl: (productName, imageUrl) =>
    api.post('/ai/analyze-url', null, { params: { product_name: productName, image_url: imageUrl } }),
  getLogs: (params) => api.get('/ai/logs', { params }),
};

// ===== STATISTICS =====
export const statsAPI = {
  getDashboard: () => api.get('/statistics/dashboard'),
  getRevenue: (period) => api.get('/statistics/revenue', { params: { period } }),
  getSellerStats: (sellerId) => api.get(`/statistics/seller/${sellerId}`),
};

// ===== LOYALTY & ACCOUNT =====
export const loyaltyAPI = {
  // Profile
  getProfile:    ()     => api.get('/loyalty/profile'),
  updateProfile: (data) => api.put('/loyalty/profile', data),
  uploadAvatar:  (url)  => api.post('/loyalty/profile/avatar', null, { params: { avatar_url: url } }),

  // Address Book
  listAddresses:    ()              => api.get('/loyalty/addresses'),
  addAddress:       (data)          => api.post('/loyalty/addresses', data),
  updateAddress:    (id, data)      => api.put(`/loyalty/addresses/${id}`, data),
  deleteAddress:    (id)            => api.delete(`/loyalty/addresses/${id}`),
  setDefaultAddr:   (id)            => api.patch(`/loyalty/addresses/${id}/default`),

  // Loyalty Points
  getPoints:          ()                       => api.get('/loyalty/points'),
  earnPoints:         (data)                   => api.post('/loyalty/points/earn', data),
  earnFromOrder:      (orderId, amount)        => api.post('/loyalty/points/earn-order', null, {
                          params: { order_id: orderId, order_amount: amount },
                        }),
  redeemPreview:      (orderAmount, points)    => api.post('/loyalty/points/redeem', {
                          order_amount: orderAmount, points_to_use: points,
                        }),
  redeemConfirm:      (orderAmount, points, orderId) => api.post('/loyalty/points/redeem/confirm', {
                          order_amount: orderAmount, points_to_use: points,
                        }, { params: { order_id: orderId } }),
  getTiers:           ()    => api.get('/loyalty/tiers'),
  listTransactions:   (limit = 20) => api.get('/loyalty/transactions', { params: { limit } }),
};
