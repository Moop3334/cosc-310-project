import { useState, useEffect } from 'react';
import { restaurantAPI, userAPI } from '../../services/api';
import RestaurantForm from './RestaurantForm';
import './styles/RestaurantOwnerDashboard.css';

export default function RestaurantOwnerDashboard() {
  const [restaurants, setRestaurants] = useState([]);
  const [editableRestaurants, setEditableRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingRestaurant, setEditingRestaurant] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all restaurants
      const allRestaurants = await restaurantAPI.getRestaurants();
      setRestaurants(allRestaurants);

      // Fetch logged-in user data to get editable restaurants
      if (username) {
        const userData = await userAPI.getUserByUsername(username);
        const userEditableIds = userData.editable_restaurants || [];
        
        // Filter restaurants that this user can edit
        const editable = allRestaurants.filter(r => 
          userEditableIds.includes(String(r.id)) || userEditableIds.includes(r.id)
        );
        setEditableRestaurants(editable);
      }
    } catch (err) {
      setError('Failed to load restaurants. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setEditingRestaurant(null);
    setShowForm(true);
  };

  const handleEdit = (restaurant) => {
    setEditingRestaurant(restaurant);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingRestaurant(null);
    fetchData();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingRestaurant(null);
  };

  const handleDeleteClick = (restaurant) => {
    setDeleteConfirm(restaurant);
  };

  const handleDeleteConfirm = async () => {
    if (!deleteConfirm) return;

    try {
      await restaurantAPI.deleteRestaurant(deleteConfirm.id);
      setDeleteConfirm(null);
      fetchData();
    } catch (err) {
      setError('Failed to delete restaurant. Please try again.');
      console.error(err);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteConfirm(null);
  };

  if (showForm) {
    return (
      <RestaurantForm
        restaurant={editingRestaurant}
        onSuccess={handleFormSuccess}
        onCancel={handleFormCancel}
      />
    );
  }

  return (
    <div className="owner-dashboard">
      <div className="dashboard-header">
        <h1>🏪 Restaurant Owner Dashboard</h1>
        <p>Manage your restaurants</p>
      </div>

      {error && <div className="dashboard-error">{error}</div>}

      {loading ? (
        <div className="loading">Loading your restaurants...</div>
      ) : (
        <div className="dashboard-content">
          <div className="section">
            <div className="section-header">
              <h2>Your Restaurants</h2>
              <button className="btn-create" onClick={handleCreateNew}>
                + Create New Restaurant
              </button>
            </div>

            {editableRestaurants.length === 0 ? (
              <div className="empty-state">
                <p>You don't have any restaurants yet.</p>
                <p>Click "Create New Restaurant" to get started!</p>
              </div>
            ) : (
              <div className="restaurants-grid">
                {editableRestaurants.map((restaurant) => (
                  <div key={restaurant.id} className="restaurant-owner-card">
                    <div className="card-header">
                      <h3>{restaurant.name}</h3>
                      <span className="restaurant-id">ID: {restaurant.id}</span>
                    </div>

                    <div className="card-content">
                      <div className="info-row">
                        <span className="label">📍 Address:</span>
                        <span className="value">{restaurant.address}</span>
                      </div>

                      <div className="info-row">
                        <span className="label">🕐 Hours:</span>
                        <span className="value">
                          {formatTime(restaurant.open_times[0])} - {formatTime(restaurant.close_times[0])}
                        </span>
                      </div>

                      <div className="info-row">
                        <span className="label">🍽️ Menu Items:</span>
                        <span className="value">{restaurant.menu?.length || 0} items</span>
                      </div>
                    </div>

                    <div className="card-actions">
                      <button 
                        className="btn-edit"
                        onClick={() => handleEdit(restaurant)}
                      >
                        Edit
                      </button>
                      <button 
                        className="btn-delete"
                        onClick={() => handleDeleteClick(restaurant)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {deleteConfirm && (
            <div className="delete-modal-overlay">
              <div className="delete-modal">
                <h3>Delete Restaurant?</h3>
                <p>
                  Are you sure you want to delete <strong>{deleteConfirm.name}</strong>? 
                  This action cannot be undone.
                </p>
                <div className="modal-actions">
                  <button 
                    className="btn-cancel"
                    onClick={handleDeleteCancel}
                  >
                    Cancel
                  </button>
                  <button 
                    className="btn-confirm-delete"
                    onClick={handleDeleteConfirm}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function formatTime(timeString) {
  if (!timeString) return 'N/A';
  return timeString.split(':').slice(0, 2).join(':');
}
