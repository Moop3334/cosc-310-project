import { useState, useEffect } from 'react';
import { restaurantAPI } from '../../services/api';
import MenuItemList from './MenuItemList';
import './styles/RestaurantDetail.css';

export default function RestaurantDetail({ restaurant, onBack }) {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchMenuItems();
  }, [restaurant.id, searchQuery]);

  const fetchMenuItems = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await restaurantAPI.getMenu(restaurant.id, searchQuery || null);
      setMenuItems(data);
    } catch (err) {
      setError('Failed to load menu items.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getDayName = (index) => {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days[index];
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return timeString.split(':').slice(0, 2).join(':');
  };

  const formatHours = () => {
    if (!restaurant.open_times || !restaurant.close_times) return 'Hours not available';
    
    return restaurant.open_times.map((openTime, index) => (
      <div key={index} className="hours-row">
        <span className="day">{getDayName(index)}:</span>
        <span className="time">
          {formatTime(openTime)} - {formatTime(restaurant.close_times[index])}
        </span>
      </div>
    ));
  };

  return (
    <div className="restaurant-detail">
      <button className="back-button" onClick={onBack}>
        ← Back to Restaurants
      </button>

      <div className="detail-header">
        <h1>{restaurant.name}</h1>
        <p className="address">📍 {restaurant.address}</p>
      </div>

      <div className="detail-content">
        <div className="info-section">
          <h2>Hours of Operation</h2>
          <div className="hours-grid">
            {formatHours()}
          </div>
        </div>

        <div className="menu-section">
          <h2>Menu</h2>
          
          <div className="menu-search">
            <input
              type="text"
              placeholder="Search menu items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="menu-search-input"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Loading menu items...</div>
          ) : menuItems.length === 0 ? (
            <div className="no-results">
              <p>No menu items found.</p>
            </div>
          ) : (
            <>
              <p className="item-count">{menuItems.length} items available</p>
              <MenuItemList items={menuItems} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
