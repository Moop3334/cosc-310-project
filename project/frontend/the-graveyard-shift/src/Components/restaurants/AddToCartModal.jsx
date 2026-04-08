import { useState } from 'react';
import './styles/AddToCartModal.css';

export default function AddToCartModal({ item, restaurantId, onAdd, onClose }) {
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);
  const [error, setError] = useState(null);

  const handleQuantityChange = (delta) => {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1) {
      setQuantity(newQuantity);
    }
  };

  const handleAddToCart = async () => {
    try {
      setIsAdding(true);
      setError(null);
      
      const userId = localStorage.getItem('userId');
      const username = localStorage.getItem('username');
      
      // Debug: Log what we have in storage
      console.log('Cart add - userId:', userId, 'username:', username);
      
      // Check for both existence AND non-empty values
      const isAuthenticated = Boolean(userId && userId.trim()) && Boolean(username && username.trim());
      
      if (!isAuthenticated) {
        setError('Authentication required. Please log in to add items to your cart.');
        setIsAdding(false);
        return;
      }

      const cartItem = {
        item_id: item.id,
        item_name: item.item_name,
        quantity: quantity,
        price: item.price,
      };

      await onAdd(userId, restaurantId, cartItem);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to add item to cart');
      console.error(err);
    } finally {
      setIsAdding(false);
    }
  };

  const totalPrice = (item.price * quantity).toFixed(2);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{item.item_name}</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          <p className="item-description">{item.description}</p>
          <p className="item-price">${item.price.toFixed(2)} each</p>

          <div className="quantity-selector">
            <label>Quantity:</label>
            <div className="quantity-controls">
              <button 
                className="qty-btn" 
                onClick={() => handleQuantityChange(-1)}
                disabled={isAdding}
              >
                −
              </button>
              <span className="quantity-display">{quantity}</span>
              <button 
                className="qty-btn" 
                onClick={() => handleQuantityChange(1)}
                disabled={isAdding}
              >
                +
              </button>
            </div>
          </div>

          <div className="price-summary">
            <span>Total:</span>
            <span className="total-price">${totalPrice}</span>
          </div>

          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="modal-footer">
          <button className="cancel-btn" onClick={onClose} disabled={isAdding}>
            Cancel
          </button>
          <button 
            className="add-btn" 
            onClick={handleAddToCart}
            disabled={isAdding}
          >
            {isAdding ? 'Adding...' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  );
}
