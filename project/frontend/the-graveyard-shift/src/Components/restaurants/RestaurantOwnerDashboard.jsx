import { useState, useEffect } from 'react';
import { restaurantAPI, userAPI, orderAPI } from '../../services/api';
import RestaurantForm from './RestaurantForm';
import './styles/RestaurantOwnerDashboard.css';

export default function RestaurantOwnerDashboard() {
  const [restaurants, setRestaurants] = useState([]);
  const [editableRestaurants, setEditableRestaurants] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingRestaurant, setEditingRestaurant] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [orderLoading, setOrderLoading] = useState(true);
  const [orderError, setOrderError] = useState(null);
  const [statusUpdates, setStatusUpdates] = useState({});

  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      setOrderLoading(true);
      setOrderError(null);

      const allRestaurants = await restaurantAPI.getRestaurants();
      const allOrders = await orderAPI.getOrders();
      setRestaurants(allRestaurants);

      if (username) {
        const userData = await userAPI.getUserByUsername(username);
        const userEditableIds = userData.editable_restaurants || [];

        const editable = allRestaurants.filter((r) =>
          userEditableIds.includes(String(r.id)) || userEditableIds.includes(r.id)
        );

        setEditableRestaurants(editable);
        const editableRestaurantIds = editable.map((restaurant) => restaurant.id);
        setOrders(allOrders.filter((order) => editableRestaurantIds.includes(order.restaurant_id)));
      } else {
        setEditableRestaurants([]);
        setOrders([]);
      }
    } catch (err) {
      setError('Failed to load restaurants. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
      setOrderLoading(false);
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

  const handleOrderStatusChange = (orderId, status) => {
    setStatusUpdates((prev) => ({
      ...prev,
      [orderId]: status,
    }));
  };

  const handleUpdateOrderStatus = async (orderId) => {
    const order = orders.find((orderItem) => orderItem.id === orderId);
    if (!order) return;
    const selectedStatus = statusUpdates[orderId] ?? order.status;
    if (selectedStatus === order.status) return;

    try {
      setError(null);
      await orderAPI.updateOrderStatus(orderId, selectedStatus);
      setOrders((prevOrders) =>
        prevOrders.map((item) =>
          item.id === orderId ? { ...item, status: selectedStatus } : item
        )
      );
      setStatusUpdates((prev) => {
        const next = { ...prev };
        delete next[orderId];
        return next;
      });
    } catch (err) {
      setError('Failed to update order status. Please try again.');
      console.error(err);
    }
  };

  const ORDER_STATUS_OPTIONS = [
    'Pending Approval',
    'Preparing',
    'Out for Delivery',
    'Cancelled'
  ];

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

      <div className="orders-section">
        <div className="section-header">
          <h2>Restaurant Orders</h2>
        </div>

        {orderError && <div className="dashboard-error">{orderError}</div>}

        {orderLoading ? (
          <div className="loading">Loading restaurant orders...</div>
        ) : orders.length === 0 ? (
          <div className="empty-state">
            <p>No orders found for your restaurants yet.</p>
          </div>
        ) : (
          <div className="orders-grid">
            {orders.map((order) => {
              const selectedStatus = statusUpdates[order.id] ?? order.status;
              const statusChanged = selectedStatus !== order.status;
              return (
                <div key={order.id} className="order-card">
                  <div className="order-header">
                    <h3>Order #{order.id}</h3>
                    <span className={`status-pill ${order.status.toLowerCase().replace(/\s+/g, '-')}`}>
                      {order.status}
                    </span>
                  </div>

                  <div className="order-details">
                    <p><strong>Restaurant ID:</strong> {order.restaurant_id}</p>
                    <p><strong>Customer ID:</strong> {order.user_id}</p>
                    <p><strong>Date:</strong> {formatDate(order.creation_date)}</p>
                    <p><strong>Total:</strong> ${order.total_price.toFixed(2)}</p>
                  </div>

                  <div className="order-items">
                    <h4>Items</h4>
                    <ul>
                      {order.items.map((item, index) => (
                        <li key={`${order.id}-${index}`}>
                          {item.quantity} × {item.item_name} (${item.price.toFixed(2)})
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="order-actions">
                    <select
                      className="status-select"
                      value={selectedStatus}
                      onChange={(e) => handleOrderStatusChange(order.id, e.target.value)}
                    >
                      {ORDER_STATUS_OPTIONS.map((status) => (
                        <option key={status} value={status}>
                          {status}
                        </option>
                      ))}
                    </select>
                    <button
                      className="btn-update"
                      disabled={!statusChanged}
                      onClick={() => handleUpdateOrderStatus(order.id)}
                    >
                      Update Status
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function formatTime(timeString) {
  if (!timeString) return 'N/A';
  return timeString.split(':').slice(0, 2).join(':');
}
