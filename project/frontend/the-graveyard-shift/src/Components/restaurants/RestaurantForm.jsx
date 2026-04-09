import { useState, useEffect } from 'react';
import { restaurantAPI, userAPI } from '../../services/api';
import './styles/RestaurantForm.css';

export default function RestaurantForm({ restaurant = null, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    open_times: Array(7).fill('09:00'),
    close_times: Array(7).fill('22:00'),
  });

  const [menuItems, setMenuItems] = useState([]);
  const [showAddMenu, setShowAddMenu] = useState(false);
  const [editingMenuItem, setEditingMenuItem] = useState(null);
  const [newMenuItem, setNewMenuItem] = useState({
    item_name: '',
    price: '',
    description: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  // Initialize form with restaurant data if editing
  useEffect(() => {
    if (restaurant) {
      setFormData({
        name: restaurant.name,
        address: restaurant.address,
        open_times: restaurant.open_times.map(t => 
          typeof t === 'string' ? t.substring(0, 5) : t
        ),
        close_times: restaurant.close_times.map(t => 
          typeof t === 'string' ? t.substring(0, 5) : t
        ),
      });
      setMenuItems(restaurant.menu || []);
    }
  }, [restaurant]);

  const handleNameChange = (e) => {
    setFormData({ ...formData, name: e.target.value });
  };

  const handleAddressChange = (e) => {
    setFormData({ ...formData, address: e.target.value });
  };

  const handleTimeChange = (type, dayIndex, value) => {
    const newTimes = [...formData[type]];
    newTimes[dayIndex] = value;
    setFormData({ ...formData, [type]: newTimes });
  };

  const handleMenuItemChange = (field, value) => {
    setNewMenuItem({ ...newMenuItem, [field]: value });
  };

  const handleAddMenuItem = () => {
    if (!newMenuItem.item_name.trim() || !newMenuItem.price) {
      setError('Menu item name and price are required');
      return;
    }

    const price = parseFloat(newMenuItem.price);
    if (isNaN(price) || price < 0) {
      setError('Price must be a valid number');
      return;
    }

    if (editingMenuItem !== null) {
      const updatedItems = [...menuItems];
      updatedItems[editingMenuItem] = {
        ...newMenuItem,
        price: price,
        id: menuItems[editingMenuItem].id,
      };
      setMenuItems(updatedItems);
      setEditingMenuItem(null);
    } else {
      setMenuItems([
        ...menuItems,
        {
          ...newMenuItem,
          price: price,
          id: Date.now(),
        },
      ]);
    }

    setNewMenuItem({ item_name: '', price: '', description: '' });
    setShowAddMenu(false);
    setError(null);
  };

  const handleEditMenuItem = (index) => {
    setEditingMenuItem(index);
    setNewMenuItem(menuItems[index]);
    setShowAddMenu(true);
  };

  const handleDeleteMenuItem = (index) => {
    setMenuItems(menuItems.filter((_, i) => i !== index));
  };

  const handleCancelAddMenu = () => {
    setShowAddMenu(false);
    setEditingMenuItem(null);
    setNewMenuItem({ item_name: '', price: '', description: '' });
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError('Restaurant name is required');
      return false;
    }
    if (!formData.address.trim()) {
      setError('Address is required');
      return false;
    }
    if (formData.open_times.some(t => !t) || formData.close_times.some(t => !t)) {
      setError('All opening and closing times are required');
      return false;
    }
    
    // Validate that closing time is after opening time for each day
    for (let i = 0; i < 7; i++) {
      if (formData.open_times[i] >= formData.close_times[i]) {
        setError(`${days[i]}: Closing time must be after opening time`);
        return false;
      }
    }
    
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);
      
      const submitData = {
        name: formData.name.trim(),
        address: formData.address.trim(),
        open_times: formData.open_times.map(t => t + ':00'),
        close_times: formData.close_times.map(t => t + ':00'),
        menu: menuItems,
      };

      if (restaurant) {
        // Update existing restaurant
        await restaurantAPI.updateRestaurant(restaurant.id, submitData);
        setSuccessMessage('Restaurant updated successfully!');
      } else {
        // Create new restaurant
        const createdRestaurant = await restaurantAPI.createRestaurant(submitData);
        
        // Add the new restaurant id to the user's editable_restaurants
        const username = localStorage.getItem('username');
        if (username && createdRestaurant.id) {
          const userData = await userAPI.getUserByUsername(username);
          const updatedEditableRestaurants = [...(userData.editable_restaurants || []), String(createdRestaurant.id)];
          await userAPI.updateUser(username, {
            editable_restaurants: updatedEditableRestaurants
          });
        }
        
        setSuccessMessage('Restaurant created successfully!');
      }

      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (err) {
      setError(err.message || 'Failed to save restaurant. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="restaurant-form-container">
      <div className="restaurant-form-card">
        <h2>{restaurant ? 'Edit Restaurant' : 'Create New Restaurant'}</h2>
        
        {error && <div className="restaurant-form-error">{error}</div>}
        {successMessage && <div className="restaurant-form-success">{successMessage}</div>}

        <form onSubmit={handleSubmit}>
          <div className="restaurant-form-group">
            <label htmlFor="name">Restaurant Name *</label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={handleNameChange}
              placeholder="Enter restaurant name"
              disabled={loading}
            />
          </div>

          <div className="restaurant-form-group">
            <label htmlFor="address">Address *</label>
            <input
              id="address"
              type="text"
              value={formData.address}
              onChange={handleAddressChange}
              placeholder="Enter restaurant address"
              disabled={loading}
            />
          </div>

          <div className="restaurant-hours-section">
            <h3>Hours of Operation</h3>
            <div className="restaurant-hours-grid">
              {days.map((day, index) => (
                <div key={day} className="restaurant-day-hours">
                  <label>{day}</label>
                  <div className="restaurant-time-inputs">
                    <input
                      type="time"
                      value={formData.open_times[index]}
                      onChange={(e) => handleTimeChange('open_times', index, e.target.value)}
                      disabled={loading}
                    />
                    <span className="restaurant-time-separator">-</span>
                    <input
                      type="time"
                      value={formData.close_times[index]}
                      onChange={(e) => handleTimeChange('close_times', index, e.target.value)}
                      disabled={loading}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="restaurant-form-menu-section">
            <h3>🍽️ Menu Items</h3>
            
            {menuItems.length > 0 ? (
              <div className="restaurant-form-menu-items-list">
                {menuItems.map((item, index) => (
                  <div key={index} className="restaurant-form-menu-item">
                    <div className="restaurant-form-menu-item-info">
                      <div className="restaurant-form-menu-item-name">{item.item_name}</div>
                      {item.description && <div className="restaurant-form-menu-item-desc">{item.description}</div>}
                      <div className="restaurant-form-menu-item-price">${parseFloat(item.price).toFixed(2)}</div>
                    </div>
                    <div className="restaurant-form-menu-item-actions">
                      <button
                        type="button"
                        className="restaurant-form-btn restaurant-form-btn-small restaurant-form-btn-edit-item"
                        onClick={() => handleEditMenuItem(index)}
                        disabled={loading}
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        className="restaurant-form-btn restaurant-form-btn-small restaurant-form-btn-delete-item"
                        onClick={() => handleDeleteMenuItem(index)}
                        disabled={loading}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="restaurant-form-no-items-message">No menu items yet. Add your first item!</div>
            )}

            {showAddMenu && (
              <div className="restaurant-form-add-menu-form">
                <h4>{editingMenuItem !== null ? 'Edit Menu Item' : 'Add New Menu Item'}</h4>
                <div className="restaurant-form-menu-row">
                  <div className="restaurant-form-group">
                    <label htmlFor="item_name">Item Name *</label>
                    <input
                      id="item_name"
                      type="text"
                      value={newMenuItem.item_name}
                      onChange={(e) => handleMenuItemChange('item_name', e.target.value)}
                      placeholder="e.g., Graveyard Burger"
                      disabled={loading}
                    />
                  </div>
                  <div className="restaurant-form-group">
                    <label htmlFor="price">Price *</label>
                    <input
                      id="price"
                      type="number"
                      step="0.01"
                      value={newMenuItem.price}
                      onChange={(e) => handleMenuItemChange('price', e.target.value)}
                      placeholder="e.g., 12.99"
                      disabled={loading}
                    />
                  </div>
                </div>
                <div className="restaurant-form-menu-row full">
                  <div className="restaurant-form-group">
                    <label htmlFor="description">Description</label>
                    <textarea
                      id="description"
                      value={newMenuItem.description}
                      onChange={(e) => handleMenuItemChange('description', e.target.value)}
                      placeholder="Optional: Describe the item"
                      disabled={loading}
                      rows="3"
                    />
                  </div>
                </div>
                <div className="restaurant-form-add-menu-actions">
                  <button
                    type="button"
                    className="restaurant-form-btn restaurant-form-btn-add-menu"
                    onClick={handleAddMenuItem}
                    disabled={loading}
                  >
                    {editingMenuItem !== null ? 'Update Item' : 'Add Item'}
                  </button>
                  <button
                    type="button"
                    className="restaurant-form-btn restaurant-form-btn-cancel-add"
                    onClick={handleCancelAddMenu}
                    disabled={loading}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {!showAddMenu && (
              <button
                type="button"
                className="restaurant-form-btn restaurant-form-btn-primary"
                onClick={() => setShowAddMenu(true)}
                disabled={loading}
                style={{ width: '100%', marginTop: '12px' }}
              >
                + Add Menu Item
              </button>
            )}
          </div>

          <div className="restaurant-form-actions">
            <button
              type="submit"
              className="restaurant-form-btn restaurant-form-btn-primary"
              disabled={loading}
            >
              {loading ? 'Saving...' : restaurant ? 'Update Restaurant' : 'Create Restaurant'}
            </button>
            <button
              type="button"
              className="restaurant-form-btn restaurant-form-btn-secondary"
              onClick={onCancel}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
