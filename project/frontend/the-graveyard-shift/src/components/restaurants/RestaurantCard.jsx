import './styles/RestaurantCard.css';

export default function RestaurantCard({ restaurant, onClick }) {
  /*const getDayName = (index) => {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days[index];
  };*/

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    // Handle both "HH:MM:SS" and "HH:MM" formats
    return timeString.split(':').slice(0, 2).join(':');
  };

  const isOpenToday = () => {
    const today = new Date().getDay();
    const adjustedDay = today === 0 ? 6 : today - 1; // Convert JS day (0=Sunday) to our format (0=Monday)
    
    if (!restaurant.open_times || !restaurant.close_times) return 'Unknown';
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const openTime = restaurant.open_times[adjustedDay];
    const closeTime = restaurant.close_times[adjustedDay];
    
    return currentTime >= openTime && currentTime < closeTime ? 'Open' : 'Closed';
  };

  return (
    <div className="restaurant-card">
      <div className="card-header">
        <h3>{restaurant.name}</h3>
        <span className={`status-badge ${isOpenToday().toLowerCase()}`}>
          {isOpenToday()}
        </span>
      </div>
      
      <div className="card-content">
        <p className="address">
          <strong>📍 Address:</strong> {restaurant.address}
        </p>
        
        <div className="hours-preview">
          <strong>Today's Hours:</strong>
          <p>
            {formatTime(restaurant.open_times?.[new Date().getDay() === 0 ? 6 : new Date().getDay() - 1])} 
            {' - '}
            {formatTime(restaurant.close_times?.[new Date().getDay() === 0 ? 6 : new Date().getDay() - 1])}
          </p>
        </div>

        {restaurant.menu && restaurant.menu.length > 0 && (
          <p className="menu-items-count">
            🍴 {restaurant.menu.length} menu items available
          </p>
        )}
      </div>

      <button className="view-menu-btn" onClick={onClick}>
        View Menu →
      </button>
    </div>
  );
}
