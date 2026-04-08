import { useEffect, useMemo, useState } from "react";
import { orderAPI, userAPI } from "../../services/api";
import "./styles/OrdersPage.css";

const COMPLETED_STATUSES = ["Completed", "Delivered", "Cancelled"];

function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userId, setUserId] = useState(localStorage.getItem("userId") || "");

  const username = localStorage.getItem("username");

  useEffect(() => {
    const resolveUserId = async () => {
      if (userId || !username) return;

      try {
        const userData = await userAPI.getUserByUsername(username);
        const resolvedId = String(userData.user_id || "");
        setUserId(resolvedId);
        localStorage.setItem("userId", resolvedId);
      } catch (err) {
        console.error("Failed to resolve userId from username:", err);
        setError("Unable to determine current user. Please sign out and sign in again.");
        setLoading(false);
      }
    };

    resolveUserId();
  }, [username, userId]);

  useEffect(() => {
    if (!userId) {
      if (!username) {
        setError("Please sign in to view your orders.");
        setLoading(false);
      }
      return;
    }

    const fetchOrders = async () => {
      setLoading(true);
      setError("");

      try {
        const data = await orderAPI.getOrders();
        const filteredOrders = data.filter((order) => String(order.user_id) === String(userId));
        setOrders(filteredOrders);
      } catch (err) {
        setError(err.message || "Unable to load orders. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [userId, username]);

  const currentOrders = useMemo(
    () => orders.filter((order) => !COMPLETED_STATUSES.includes(order.status)),
    [orders]
  );

  const pastOrders = useMemo(
    () => orders.filter((order) => COMPLETED_STATUSES.includes(order.status)),
    [orders]
  );

  const renderOrderItems = (order) => {
    if (!Array.isArray(order.items) || order.items.length === 0) {
      return <p className="empty-message">No items available for this order.</p>;
    }

    return (
      <ul className="order-items-list">
        {order.items.map((item) => (
          <li key={`${item.item_id}-${item.quantity}`}>
            <span className="item-name">{item.item_name}</span>
            <span className="item-quantity">x{item.quantity}</span>
            <span className="item-price">${item.price.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    );
  };

  const renderSection = (title, orderList) => (
    <div className="orders-section">
      <h2>{title}</h2>
      {orderList.length === 0 ? (
        <p className="empty-message">No orders in this section yet.</p>
      ) : (
        <div className="orders-grid">
          {orderList.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-card-header">
                <div>
                  <span className="order-id">Order #{order.id}</span>
                  <span className={`order-status ${order.status.toLowerCase().replace(/\s+/g, "-")}`}>
                    {order.status}
                  </span>
                </div>
                <div className="order-date">
                  {new Date(order.creation_date).toLocaleString()}
                </div>
              </div>
              <div className="order-details">
                <div className="order-detail-row">
                  <strong>Restaurant ID:</strong>
                  <span>{order.restaurant_id}</span>
                </div>
                <div className="order-detail-row">
                  <strong>Total:</strong>
                  <span>${order.total_price.toFixed(2)}</span>
                </div>
                <div className="order-detail-row">
                  <strong>Items:</strong>
                  <span>{order.items.length}</span>
                </div>
              </div>
              {renderOrderItems(order)}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="orders-page-container">
      <div className="orders-page-header">
        <div>
          <h1>My Orders</h1>
          <p>Track your current deliveries and review previously completed orders.</p>
        </div>
      </div>

      {loading ? (
        <div className="status-message">Loading your orders...</div>
      ) : error ? (
        <div className="status-message error">{error}</div>
      ) : (
        <>
          {renderSection("Current Orders", currentOrders)}
          {renderSection("Past Orders", pastOrders)}
        </>
      )}
    </div>
  );
}

export default OrdersPage;
