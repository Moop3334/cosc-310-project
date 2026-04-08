import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/MenuItem.css';
import AddToCartModal from './AddToCartModal';
import { cartAPI } from '../../services/api';

export default function MenuItem({ item, restaurantId, onAddSuccess }) {
  const [showModal, setShowModal] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const navigate = useNavigate();

  const handleAddToCartClick = () => {
    const userId = localStorage.getItem('userId');
    const username = localStorage.getItem('username');
    
    // Debug: Log what we have in storage
    console.log('Auth check - userId:', userId, 'username:', username);
    
    // Check for both existence AND non-empty values
    // userId must be a valid string that's not empty
    const isAuthenticated = Boolean(userId && userId.trim()) && Boolean(username && username.trim());
    
    if (!isAuthenticated) {
      console.warn('Authentication failed - missing or empty credentials');
      alert('Please log in to add items to your cart');
      navigate('/login');
      return;
    }
    
    setShowModal(true);
  };

  const handleAddToCart = async (userId, restaurantId, cartItem) => {
    try {
      setIsAdding(true);
      await cartAPI.addToCart(userId, restaurantId, cartItem);
      if (onAddSuccess) {
        onAddSuccess(cartItem);
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      throw error;
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <>
      <div className="menu-item">
        <div className="item-header">
          <h3>{item.item_name}</h3>
          <span className="price">${item.price.toFixed(2)}</span>
        </div>
        <p className="description">{item.description}</p>
        <button 
          className="add-to-cart-btn"
          onClick={handleAddToCartClick}
          disabled={isAdding}
        >
          {isAdding ? 'Adding...' : 'Add to Cart'}
        </button>
      </div>

      {showModal && (
        <AddToCartModal
          item={item}
          restaurantId={restaurantId}
          onAdd={handleAddToCart}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
