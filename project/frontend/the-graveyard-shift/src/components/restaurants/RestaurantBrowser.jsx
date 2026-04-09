import { useState, useEffect } from 'react';
import { restaurantAPI, recommendationAPI } from '../../services/api';
import RestaurantList from './RestaurantList';
import RestaurantDetail from './RestaurantDetail';
import './styles/RestaurantBrowser.css';

export default function RestaurantBrowser() {
  const [restaurants, setRestaurants] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch restaurants on component mount or when search query changes
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    fetchRestaurantsAndRecommendations();
  }, [searchQuery]);

  const fetchRestaurantsAndRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);

      const restaurantData = await restaurantAPI.getRestaurants(searchQuery || null);
      setRestaurants(restaurantData);
      setSelectedRestaurant(null);

      if (userId && !searchQuery) {
        try {
          const recommendationData = await recommendationAPI.getRecommendations(userId);
          setRecommendations(recommendationData);
        } catch (recErr) {
          console.error('Failed to load recommendations:', recErr);
          setRecommendations([]);
        }
      } else {
        setRecommendations([]);
      }
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

  const handleRecommendedClick = (recommendedRestaurantId) => {
    const matchedRestaurant = restaurants.find(
      (restaurant) => String(restaurant.id) === String(recommendedRestaurantId)
    );

    if (matchedRestaurant) {
      handleSelectRestaurant(matchedRestaurant);
    }
  };

  const renderRecommendations = () => {
    if (searchQuery) {
      return null;
    }

    return (
      <div className="recommended-section">
        <h2>Recommended for You</h2>
        {recommendations.length === 0 ? (
          <p className="no-results">
            No recommendations yet. Complete some orders first.
          </p>
        ) : (
          <div className="recommended-grid">
            {recommendations.map((rec) => (
              <button
                key={rec.restaurant_id}
                type="button"
                className="recommended-card"
                onClick={() => handleRecommendedClick(rec.restaurant_id)}
              >
                <h3>{rec.restaurant_name}</h3>
                <p><strong>Address:</strong> {rec.address}</p>
                <p><strong>Ordered Before:</strong> {rec.order_count} time(s)</p>
                <p><strong>Click to view menu</strong></p>
              </button>
            ))}
          </div>
        )}
      </div>
    );
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

            {renderRecommendations()}

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