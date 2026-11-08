// Store đơn giản dùng localStorage + React Context
// (có thể nâng cấp lên Zustand/Redux sau)

export const getToken = () => localStorage.getItem('agrixanh_token');
export const getUser = () => {
  try {
    return JSON.parse(localStorage.getItem('agrixanh_user') || 'null');
  } catch {
    return null;
  }
};
export const setAuth = (token, user) => {
  localStorage.setItem('agrixanh_token', token);
  localStorage.setItem('agrixanh_user', JSON.stringify(user));
};
export const clearAuth = () => {
  localStorage.removeItem('agrixanh_token');
  localStorage.removeItem('agrixanh_user');
};

// Cart store
export const getCart = () => {
  try {
    return JSON.parse(localStorage.getItem('agrixanh_cart') || '[]');
  } catch {
    return [];
  }
};
export const saveCart = (cart) => {
  localStorage.setItem('agrixanh_cart', JSON.stringify(cart));
};
export const addToCart = (product, quantity = 1) => {
  const cart = getCart();
  const pid = product.id || product._id;
  const existing = cart.find((i) => i.product_id === pid);
  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({
      product_id: pid,
      product_name: product.name,
      quantity,
      unit_price: product.price,
      seller_id: product.seller_id || 'user_seller_001',
      unit: product.unit || 'kg',
      image_url: product.image_url || '',
    });
  }
  saveCart(cart);
  return cart;
};
export const removeFromCart = (productId) => {
  const cart = getCart().filter((i) => i.product_id !== productId);
  saveCart(cart);
  return cart;
};
export const clearCart = () => saveCart([]);
export const getCartTotal = () =>
  getCart().reduce((sum, i) => sum + i.quantity * i.unit_price, 0);
