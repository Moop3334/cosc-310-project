import { useState, useEffect } from 'react';
import { orderAPI } from '../../services/api';
import './styles/DeliveryDriverDashboard.css';

const DELIVERY_STATUSES = [
  'Pending Approval',
  'Preparing',
  'Out for Delivery',
  'Delivered',
  'Cancelled'
];

const STATUS_COLORS = {
  'pending approval': 'pending-approval',
  'preparing': 'preparing',
  'out for delivery': 'out-for-delivery',
  'delivered': 'delivered',
  'cancelled': 'cancelled'
};

export default function DeliveryDriverDashboard() {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusUpdates, setStatusUpdates] = useState({});
  const [updatingOrderId, setUpdatingOrderId] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('recent');

  useEffect(() => {
    fetchOrders();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [orders, filterStatus, searchQuery, sortBy]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await orderAPI.getOrders();
      // For delivery drivers, we show orders that are either "Out for Delivery" or "Preparing"
      // or any status so they can manage all stages
      setOrders(data);
    } catch (err) {
      setError(err.message || 'Failed to load orders');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let filtered = [...orders];

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter((order) => order.status === filterStatus);
    }

    // Filter by search query (order ID or restaurant ID)
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter((order) =>
        order.id.toString().includes(query) ||
        order.restaurant_id.toString().includes(query) ||
        order.user_id.toString().includes(query)
      );
    }

    // Sort
    if (sortBy === 'recent') {
      filtered.sort(
        (a, b) => new Date(b.creation_date) - new Date(a.creation_date)
      );
    } else if (sortBy === 'oldest') {
      filtered.sort(
        (a, b) => new Date(a.creation_date) - new Date(b.creation_date)
      );
    } else if (sortBy === 'order-id') {
      filtered.sort((a, b) => a.id - b.id);
    }

    setFilteredOrders(filtered);
  };

  const handleStatusChange = (orderId, newStatus) => {
    setStatusUpdates((prev) => ({
      ...prev,
      [orderId]: newStatus,
    }));
  };

  const handleUpdateStatus = async (orderId) => {
    const newStatus = statusUpdates[orderId];
    if (!newStatus) return;

    try {
      setUpdatingOrderId(orderId);
      await orderAPI.updateOrderStatus(orderId, newStatus);
      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.id === orderId ? { ...order, status: newStatus } : order
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
    } finally {
      setUpdatingOrderId(null);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderOrderCard = (order) => {
    const selectedStatus = statusUpdates[order.id] ?? order.status;
    const hasChanged = selectedStatus !== order.status;

    return (
      <div key={order.id} className="driver-order-card">
        <div className="driver-card-header">
          <div className="driver-order-info">
            <h3>Order #{order.id}</h3>
            <p className="driver-restaurant-info">
              Restaurant ID: {order.restaurant_id} | Customer ID: {order.user_id}
            </p>
          </div>
          <span
            className={`driver-status-badge ${STATUS_COLORS[order.status.toLowerCase()]}`}
          >
            {order.status}
          </span>
        </div>

        <div className="driver-card-content">
          <div className="driver-order-date">
            📅 {formatDate(order.creation_date)}
          </div>

          <div className="driver-order-amount">
            💰 Total: ${order.total_price.toFixed(2)}
          </div>

          <div className="driver-order-items">
            <h4>🍽️ Items ({order.items.length})</h4>
            <ul>
              {order.items.map((item, index) => (
                <li key={`${order.id}-${index}`}>
                  <span className="driver-item-name">{item.item_name}</span>
                  <span className="driver-item-detail">
                    {item.quantity}x @ ${item.price.toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="driver-card-footer">
          <div className="driver-status-update-group">
            <select
              className="driver-status-select"
              value={selectedStatus}
              onChange={(e) => handleStatusChange(order.id, e.target.value)}
            >
              {DELIVERY_STATUSES.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
            {hasChanged && (
              <button
                className="driver-btn-update"
                onClick={() => handleUpdateStatus(order.id)}
                disabled={updatingOrderId === order.id}
              >
                {updatingOrderId === order.id ? '⏳ Updating...' : '✓ Update'}
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="delivery-driver-dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>🚚 Delivery Driver Dashboard</h1>
          <p>Manage delivery orders and update statuses</p>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="controls-section">
        <div className="search-group">
          <input
            type="text"
            placeholder="Search by Order ID, Restaurant ID, or Customer ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filters-group">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            {DELIVERY_STATUSES.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="filter-select"
          >
            <option value="recent">Most Recent</option>
            <option value="oldest">Oldest First</option>
            <option value="order-id">Order ID</option>
          </select>
        </div>
      </div>

      <div className="content-section">
        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading delivery orders...</p>
          </div>
        ) : error ? (
          <div className="error-state">
            <p>Unable to load orders. Please try again.</p>
            <button onClick={fetchOrders} className="retry-button">
              Retry
            </button>
          </div>
        ) : filteredOrders.length === 0 ? (
          <div className="empty-state">
            <p className="empty-icon">📦</p>
            <p className="empty-title">No Orders Found</p>
            <p className="empty-description">
              {searchQuery || filterStatus !== 'all'
                ? 'Try adjusting your filters or search query'
                : 'No delivery orders available at this time'}
            </p>
          </div>
        ) : (
          <div className="orders-container">
            <div className="orders-count">
              Showing {filteredOrders.length} order{filteredOrders.length !== 1 ? 's' : ''}
            </div>
            <div className="orders-grid">
              {filteredOrders.map((order) => renderOrderCard(order))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
