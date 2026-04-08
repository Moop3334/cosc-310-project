import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cartAPI, restaurantAPI } from '../../services/api';
import './styles/Cart.css';

export default function Cart() {
  const [cart, setCart] = useState(null);
  const [cartSummary, setCartSummary] = useState(null);
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const navigate = useNavigate();

  const userId = localStorage.getItem('userId');
  const username = localStorage.getItem('username');

  useEffect(() => {
    // Debug: Log what we have in storage
    console.log('Cart page - userId:', userId, 'username:', username);
    
    // Check for both existence AND non-empty values
    const isAuthenticated = Boolean(userId && userId.trim()) && Boolean(username && username.trim());
    
    if (!isAuthenticated) {
      console.warn('User not authenticated - userId:', userId, 'username:', username);
      navigate('/login');
      return;
    }
    fetchCart();
  }, [userId, username, navigate]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      setError(null);
      const cartData = await cartAPI.getCart(userId);
      setCart(cartData);

      if (cartData && cartData.restaurant_id) {
        const restaurantData = await restaurantAPI.getRestaurantById(cartData.restaurant_id);
        setRestaurant(restaurantData);
      }

      const summaryData = await cartAPI.getCartSummary(userId);
      setCartSummary(summaryData);
    } catch (err) {
      setError(err.message || 'Failed to load cart');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      setIsUpdating(true);
      await cartAPI.removeAllItems(userId, itemId);
      await fetchCart();
    } catch (err) {
      setError('Failed to remove item from cart');
      console.error(err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDecreaseQuantity = async (itemId) => {
    try {
      setIsUpdating(true);
      await cartAPI.removeItem(userId, itemId);
      await fetchCart();
    } catch (err) {
      setError('Failed to update item quantity');
      console.error(err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleIncreaseQuantity = async (itemId) => {
    try {
      setIsUpdating(true);
      if (!cart || !cart.restaurant_id) {
        setError('Cannot increase quantity: restaurant information missing');
        return;
      }

      // Find the item to get its details
      const item = cart.items.find(i => i.item_id === itemId);
      if (!item) {
        setError('Item not found in cart');
        return;
      }

      // Use add_to_cart endpoint with quantity 1 to increase the item quantity
      await cartAPI.addToCart(userId, cart.restaurant_id, {
        item_id: itemId,
        item_name: item.item_name,
        quantity: 1,
        price: item.price,
      });

      await fetchCart();
    } catch (err) {
      setError('Failed to increase item quantity');
      console.error(err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleClearCart = async () => {
    if (window.confirm('Are you sure you want to clear your entire cart?')) {
      try {
        setIsUpdating(true);
        await cartAPI.clearCart(userId);
        setCart(null);
        setCartSummary(null);
        setRestaurant(null);
      } catch (err) {
        setError('Failed to clear cart');
        console.error(err);
      } finally {
        setIsUpdating(false);
      }
    }
  };

  const handleCheckout = () => {
    // This would navigate to a checkout page
    navigate('/checkout');
  };

  if (loading) {
    return <div className="cart-container"><div className="loading">Loading your cart...</div></div>;
  }

  if (!cart || !cartSummary || cart.items.length === 0) {
    return (
      <div className="cart-container">
        <div className="cart-header">
          <h1>🛒 My Shopping Cart</h1>
          <button className="back-btn" onClick={() => navigate('/restaurants')}>
            ← Continue Shopping
          </button>
        </div>
        <div className="empty-cart">
          <p>Your cart is empty</p>
          <button className="continue-shopping-btn" onClick={() => navigate('/restaurants')}>
            Start Shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-container">
      <div className="cart-header">
        <h1>🛒 My Shopping Cart</h1>
        <button className="back-btn" onClick={() => navigate('/restaurants')}>
          ← Continue Shopping
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="cart-content">
        <div className="cart-items-section">
          {restaurant && (
            <div className="restaurant-info">
              <h2>From: {restaurant.name}</h2>
              <p>{restaurant.address}</p>
            </div>
          )}

          <div className="cart-items">
            <div className="items-header">
              <span>Item</span>
              <span>Price</span>
              <span>Quantity</span>
              <span>Subtotal</span>
              <span>Actions</span>
            </div>

            {cart.items.map((item) => (
              <div key={item.item_id} className="cart-item">
                <div className="item-name">{item.item_name}</div>
                <div className="item-price">${item.price.toFixed(2)}</div>
                <div className="item-quantity">
                  <button
                    className="qty-btn"
                    onClick={() => handleDecreaseQuantity(item.item_id)}
                    disabled={isUpdating}
                  >
                    −
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    className="qty-btn"
                    onClick={() => handleIncreaseQuantity(item.item_id)}
                    disabled={isUpdating}
                    title="Increase quantity by adding more from the menu"
                  >
                    +
                  </button>
                </div>
                <div className="item-subtotal">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
                <button
                  className="remove-btn"
                  onClick={() => handleRemoveItem(item.item_id)}
                  disabled={isUpdating}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          {cart.items.length > 0 && (
            <button
              className="clear-cart-btn"
              onClick={handleClearCart}
              disabled={isUpdating}
            >
              Clear Cart
            </button>
          )}
        </div>

        <div className="cart-summary-section">
          <div className="summary-card">
            <h3>Order Summary</h3>

            <div className="summary-row">
              <span>Subtotal:</span>
              <span>${cartSummary.subtotal?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row">
              <span>Tax (5%):</span>
              <span>${cartSummary.tax?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row">
              <span>Delivery Fee:</span>
              <span>${cartSummary.delivery_fee?.toFixed(2) || '0.00'}</span>
            </div>

            <div className="summary-row total">
              <span>Total:</span>
              <span>${cartSummary.total_with_fees?.toFixed(2) || '0.00'}</span>
            </div>

            <button
              className="checkout-btn"
              onClick={handleCheckout}
              disabled={isUpdating || cart.items.length === 0}
            >
              Proceed to Checkout
            </button>

            <button
              className="continue-shopping-btn"
              onClick={() => navigate('/restaurants')}
              disabled={isUpdating}
            >
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
