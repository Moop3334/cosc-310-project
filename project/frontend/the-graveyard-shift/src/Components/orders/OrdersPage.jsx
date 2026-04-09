import { useEffect, useMemo, useState } from "react";
import { orderAPI, userAPI, reviewAPI } from "../../services/api";
import ReviewForm from "../reviews/ReviewForm";
import ReviewList from "../reviews/ReviewList";
import "./styles/OrdersPage.css";

const COMPLETED_STATUSES = ["Completed", "Delivered", "Cancelled"];
const ORDER_STATUS_OPTIONS = [
  "Pending Approval",
  "Preparing",
  "Out for Delivery",
  "Delivered",
  "Cancelled"
];

function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userId, setUserId] = useState(localStorage.getItem("userId") || "");
  const [userReviews, setUserReviews] = useState([]);
  const [expandedOrder, setExpandedOrder] = useState(null);
  const [statusUpdates, setStatusUpdates] = useState({});
  const [updatingOrderId, setUpdatingOrderId] = useState(null);

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
      
      try {
        const reviews = await reviewAPI.getUserReviews(userId);
        setUserReviews(reviews);
      } catch {
        setUserReviews([]);
      }
    };

    fetchOrders();
  }, [userId, username]);

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
      setError("Failed to update order status. Please try again.");
      console.error(err);
    } finally {
      setUpdatingOrderId(null);
    }
  };

  const currentOrders = useMemo(
    () => orders.filter((order) => !COMPLETED_STATUSES.includes(order.status)),
    [orders]
  );

  const pastOrders = useMemo(
    () => orders.filter((order) => COMPLETED_STATUSES.includes(order.status)),
    [orders]
  );

  const refreshReviews = async () => {
    if (!userId) return;
    try {
      const reviews = await reviewAPI.getUserReviews(userId);
      setUserReviews(reviews);
    } catch (err) {
      console.error("Failed to refresh reviews:", err);
    }
  };

  const toggleReviewPanel = (orderId) => {
    setExpandedOrder((prev) => (prev === orderId ? null : orderId));
  };

  const getOrderReviews = (orderId) => {
    return userReviews.filter((r) => r.order_id === orderId);
  };

  const renderOrderItems = (order) => {
    if (!Array.isArray(order.items) || order.items.length === 0) {
      return <p className="user-empty-message">No items available for this order.</p>;
    }

    return (
      <ul className="order-items-list">
        {order.items.map((item) => (
          <li key={`${item.item_id}-${item.quantity}`}>
            <span className="user-item-name">{item.item_name}</span>
            <span className="user-item-quantity">x{item.quantity}</span>
            <span className="user-item-price">${item.price.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    );
  };

  const renderStatusUpdate = (order) => {
    const selectedStatus = statusUpdates[order.id] ?? order.status;
    const hasChanged = selectedStatus !== order.status;

    return (
      <div className="user-order-status-update">
        <select
          className="user-status-select"
          value={selectedStatus}
          onChange={(e) => handleStatusChange(order.id, e.target.value)}
        >
          {ORDER_STATUS_OPTIONS.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
        {hasChanged && (
          <button
            className="user-btn-update-status"
            onClick={() => handleUpdateStatus(order.id)}
            disabled={updatingOrderId === order.id}
          >
            {updatingOrderId === order.id ? "Updating..." : "Update"}
          </button>
        )}
      </div>
    );
  };

  const renderSection = (title, orderList, showReviews = false) => (
    <div className="user-orders-section">
      <h2>{title}</h2>
      {orderList.length === 0 ? (
        <p className="user-empty-message">No orders in this section yet.</p>
      ) : (
        <div className="user-orders-grid">
          {orderList.map((order) => {
            const orderReviews = getOrderReviews(order.id);
            const isExpanded = expandedOrder === order.id;

            return (
              <div key={order.id} className="user-order-card">
              <div className="order-card-header">
                <div>
                    <span className="user-order-id">Order #{order.id}</span>
                    <span className={`user-order-status ${order.status.toLowerCase().replace(/\s+/g, "-")}`}>
                    {order.status}
                  </span>
                </div>
                  <div className="user-order-date">
                  {new Date(order.creation_date).toLocaleString()}
                </div>
              </div>
              <div className="order-details">
                  <div className="user-order-detail-row">
                  <strong>Restaurant ID:</strong>
                  <span>{order.restaurant_id}</span>
                </div>
                  <div className="user-order-detail-row">
                  <strong>Total:</strong>
                  <span>${order.total_price.toFixed(2)}</span>
                </div>
                  <div className="user-order-detail-row">
                  <strong>Items:</strong>
                  <span>{order.items.length}</span>
                </div>
              </div>
              {renderOrderItems(order)}
              {renderStatusUpdate(order)}

              {showReviews && order.status !== "Cancelled" && (
                  <div className="user-review-section">
                    <button
                      className="user-toggle-review-btn"
                      onClick={() => toggleReviewPanel(order.id)}
                    >
                      {isExpanded ? "Hide Reviews" : "Write a Review"}
                    </button>

                    {isExpanded && (
                      <>
                        {orderReviews.length > 0 && (
                          <div className="user-existing-reviews">
                            <h4>Your Reviews</h4>
                            <ReviewList reviews={orderReviews} />
                          </div>
                        )}
                        <ReviewForm
                          order={order}
                          existingReviews={userReviews}
                          onReviewSubmitted={refreshReviews}
                        />
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );

  return (
    <div className="user-orders-page-container">
      <div className="orders-page-header">
        <div>
          <h1>My Orders</h1>
          <p>Track your current deliveries and review previously completed orders.</p>
        </div>
      </div>

      {loading ? (
        <div className="user-status-message">Loading your orders...</div>
      ) : error ? (
        <div className="user-status-message user-error">{error}</div>
      ) : (
        <>
          {renderSection("Current Orders", currentOrders)}
          {renderSection("Past Orders", pastOrders, true)}
        </>
      )}
    </div>
  );
}

export default OrdersPage;