import { useState, useEffect } from 'react';
import { restaurantAPI } from '../../services/api';
import RestaurantList from './RestaurantList';
import RestaurantDetail from './RestaurantDetail';
import './styles/RestaurantBrowser.css';

export default function RestaurantBrowser() {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch restaurants on component mount or when search query changes
  useEffect(() => {
    fetchRestaurants();
  }, [searchQuery]);

  const fetchRestaurants = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await restaurantAPI.getRestaurants(searchQuery || null);
      setRestaurants(data);
      setSelectedRestaurant(null); // Clear selected restaurant when search changes
    } catch (err) {
      setError('Failed to load restaurants. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  const handleSelectRestaurant = (restaurant) => {
    setSelectedRestaurant(restaurant);
  };

  const handleBackToList = () => {
    setSelectedRestaurant(null);
  };

  return (
    <div className="restaurant-browser">
      <div className="browser-header">
        <h1>🍽️ The Graveyard Shift - Restaurant Browser</h1>
        <p>Explore restaurants and discover amazing food options</p>
      </div>

      <div className="browser-content">
        {selectedRestaurant ? (
          <RestaurantDetail 
            restaurant={selectedRestaurant} 
            onBack={handleBackToList}
          />
        ) : (
          <div className="restaurant-list-section">
            <div className="search-section">
              <input
                type="text"
                placeholder="Search restaurants by name..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="search-input"
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            {loading ? (
              <div className="loading">Loading restaurants...</div>
            ) : restaurants.length === 0 ? (
              <div className="no-results">
                <p>No restaurants found. Try a different search term.</p>
              </div>
            ) : (
              <RestaurantList 
                restaurants={restaurants}
                onSelectRestaurant={handleSelectRestaurant}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
