import { useState } from 'react';
import './styles/MenuItem.css';
import AddToCartModal from './AddToCartModal';
import { cartAPI } from '../../services/api';

export default function MenuItem({ item, restaurantId, onAddSuccess }) {
  const [showModal, setShowModal] = useState(false);
  const [isAdding, setIsAdding] = useState(false);

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
          onClick={() => setShowModal(true)}
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
