import RestaurantCard from './RestaurantCard';
import './styles/RestaurantList.css';

export default function RestaurantList({ restaurants, onSelectRestaurant }) {
  return (
    <div className="restaurant-list">
      <h2>Available Restaurants</h2>
      <div className="restaurants-grid">
        {restaurants.map((restaurant) => (
          <RestaurantCard
            key={restaurant.id}
            restaurant={restaurant}
            onClick={() => onSelectRestaurant(restaurant)}
          />
        ))}
      </div>
    </div>
  );
}
