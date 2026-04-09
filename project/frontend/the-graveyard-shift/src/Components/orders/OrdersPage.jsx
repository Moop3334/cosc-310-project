import { useEffect, useMemo, useState } from "react";
import { orderAPI, userAPI, reviewAPI } from "../../services/api";
import ReviewForm from "../reviews/ReviewForm";
import ReviewList from "../reviews/ReviewList";
import "./styles/OrdersPage.css";

const COMPLETED_STATUSES = ["Completed", "Delivered", "Cancelled"];

function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [userId, setUserId] = useState(localStorage.getItem("userId") || "");
  const [userReviews, setUserReviews] = useState([]);
  const [expandedOrder, setExpandedOrder] = useState(null);

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
      <ul className="user-order-items-list">
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
                <div className="user-order-card-header">
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
                <div className="user-order-details">
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
      <div className="user-orders-page-header">
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