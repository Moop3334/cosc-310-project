import { useState, useEffect } from "react";
import "./styles/AdminPage.css";

function AdminPage() {
  const [role, setRole] = useState(localStorage.getItem("role"));
  const [restaurants, setRestaurants] = useState([]);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [editingRestaurant, setEditingRestaurant] = useState(null);
  const [editingOrder, setEditingOrder] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [expandedRestaurant, setExpandedRestaurant] = useState(null);
  const [expandedOrder, setExpandedOrder] = useState(null);
  const [expandedUser, setExpandedUser] = useState(null);

  const fetchRestaurants = async () => {
    try {
      const response = await fetch("/api/restaurants");
      const data = await response.json();
      setRestaurants(data);
    } catch (error) {
      console.error("Error fetching restaurants:", error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await fetch("/api/orders");
      const data = await response.json();
      setOrders(data);
    } catch (error) {
      console.error("Error fetching orders:", error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch("/api/users");
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  useEffect(() => {
    if (role === "admin") {
      fetchRestaurants();
      fetchOrders();
      fetchUsers();
    }
  }, [role]);

  const handleEditRestaurant = (restaurant) => {
    setEditingRestaurant({ ...restaurant });
    setExpandedRestaurant(restaurant.id);
  };

  const handleSaveRestaurant = async () => {
    try {
      await fetch(`/api/restaurants/${editingRestaurant.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingRestaurant),
      });
      setEditingRestaurant(null);
      setExpandedRestaurant(null);
      fetchRestaurants();
    } catch (error) {
      console.error("Error saving restaurant:", error);
    }
  };

  const handleEditOrder = (order) => {
    setEditingOrder({ ...order });
    setExpandedOrder(order.id);
  };

  const handleSaveOrder = async () => {
    try {
      await fetch(`/api/orders/${editingOrder.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingOrder),
      });
      setEditingOrder(null);
      setExpandedOrder(null);
      fetchOrders();
    } catch (error) {
      console.error("Error saving order:", error);
    }
  };

  const handleEditUser = (user) => {
    setEditingUser({ ...user });
    setExpandedUser(user.user_id);
  };

  const handleSaveUser = async () => {
    try {
      await fetch(`/api/users/id/${editingUser.user_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingUser),
      });
      setEditingUser(null);
      setExpandedUser(null);
      fetchUsers();
    } catch (error) {
      console.error("Error saving user:", error);
    }
  };

  const handleDeleteRestaurant = async (restaurantId) => {
    if (window.confirm("Are you sure you want to delete this restaurant?")) {
      try {
        await fetch(`/api/restaurants/${restaurantId}`, {
          method: "DELETE",
        });
        fetchRestaurants();
      } catch (error) {
        console.error("Error deleting restaurant:", error);
      }
    }
  };

  const handleDeleteOrder = async (orderId) => {
    if (window.confirm("Are you sure you want to delete this order?")) {
      try {
        await fetch(`/api/orders/${orderId}`, {
          method: "DELETE",
        });
        fetchOrders();
      } catch (error) {
        console.error("Error deleting order:", error);
      }
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm("Are you sure you want to delete this user?")) {
      try {
        await fetch(`/api/users/id/${userId}`, {
          method: "DELETE",
        });
        fetchUsers();
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    }
  };

  const renderEditField = (key, value, onChange) => {
    // Skip complex nested objects
    if (typeof value === "object" && !Array.isArray(value)) {
      return (
        <div key={key} className="edit-field">
          <label>{key}:</label>
          <textarea
            value={JSON.stringify(value, null, 2)}
            onChange={(e) => {
              try {
                onChange(JSON.parse(e.target.value));
              } catch (error) {
                // Keep original on parse error
              }
            }}
            rows="4"
          />
        </div>
      );
    }

    // Handle arrays
    if (Array.isArray(value)) {
      return (
        <div key={key} className="edit-field">
          <label>{key}:</label>
          <textarea
            value={JSON.stringify(value, null, 2)}
            onChange={(e) => {
              try {
                onChange(JSON.parse(e.target.value));
              } catch (error) {
                // Keep original on parse error
              }
            }}
            rows="4"
          />
        </div>
      );
    }

    // Handle booleans
    if (typeof value === "boolean") {
      return (
        <div key={key} className="edit-field">
          <label>{key}:</label>
          <input
            type="checkbox"
            checked={value}
            onChange={(e) => onChange(e.target.checked)}
          />
        </div>
      );
    }

    // Handle numbers
    if (typeof value === "number") {
      return (
        <div key={key} className="edit-field">
          <label>{key}:</label>
          <input
            type="number"
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
          />
        </div>
      );
    }

    // Default to text input
    return (
      <div key={key} className="edit-field">
        <label>{key}:</label>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      </div>
    );
  };

  if (role !== "admin") {
    return (
      <div className="access-denied">
        <h1>Access Denied</h1>
        <p>You do not have admin privileges.</p>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <p>Manage all restaurants, orders, and users</p>
      </div>

      <div className="admin-section">
        <h2>Restaurants ({restaurants.length})</h2>
        <div className="admin-list">
          {restaurants.map((restaurant) => (
            <div key={restaurant.id} className="admin-item">
              {editingRestaurant?.id === restaurant.id ? (
                <div className="edit-form">
                  <h3>Editing: {restaurant.name}</h3>
                  <div className="edit-fields">
                    {Object.keys(editingRestaurant).map((key) => {
                      // Skip id and menu for now (complex editing)
                      if (key === "id" || key === "menu") return null;
                      return renderEditField(
                        key,
                        editingRestaurant[key],
                        (value) =>
                          setEditingRestaurant({
                            ...editingRestaurant,
                            [key]: value,
                          })
                      );
                    })}
                  </div>
                  <div className="button-group">
                    <button className="save-btn" onClick={handleSaveRestaurant}>
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      onClick={() => {
                        setEditingRestaurant(null);
                        setExpandedRestaurant(null);
                      }}
                    >
                      Cancel
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => {
                        setEditingRestaurant(null);
                        setExpandedRestaurant(null);
                        handleDeleteRestaurant(restaurant.id);
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ) : (
                <div className="item-summary">
                  <div className="item-info">
                    <strong>ID: {restaurant.id}</strong> - {restaurant.name}
                  </div>
                  <div className="item-details">{restaurant.address}</div>
                  <div className="summary-buttons">
                    <button
                      className="edit-btn"
                      onClick={() => handleEditRestaurant(restaurant)}
                    >
                      Edit All Attributes
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDeleteRestaurant(restaurant.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="admin-section">
        <h2>Orders ({orders.length})</h2>
        <div className="admin-list">
          {orders.map((order) => (
            <div key={order.id} className="admin-item">
              {editingOrder?.id === order.id ? (
                <div className="edit-form">
                  <h3>Editing Order: {order.id}</h3>
                  <div className="edit-fields">
                    {Object.keys(editingOrder).map((key) => {
                      // Skip complex items array for basic editing
                      if (key === "items") return null;
                      return renderEditField(
                        key,
                        editingOrder[key],
                        (value) =>
                          setEditingOrder({
                            ...editingOrder,
                            [key]: value,
                          })
                      );
                    })}
                  </div>
                  <div className="button-group">
                    <button className="save-btn" onClick={handleSaveOrder}>
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      onClick={() => {
                        setEditingOrder(null);
                        setExpandedOrder(null);
                      }}
                    >
                      Cancel
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => {
                        setEditingOrder(null);
                        setExpandedOrder(null);
                        handleDeleteOrder(order.id);
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ) : (
                <div className="item-summary">
                  <div className="item-info">
                    <strong>Order ID: {order.id}</strong> - User: {order.user_id} -
                    Restaurant: {order.restaurant_id}
                  </div>
                  <div className="item-details">Status: {order.status}</div>
                  <div className="item-details">Total: ${order.total_price}</div>
                  <div className="summary-buttons">
                    <button
                      className="edit-btn"
                      onClick={() => handleEditOrder(order)}
                    >
                      Edit All Attributes
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDeleteOrder(order.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="admin-section">
        <h2>Users ({users.length})</h2>
        <div className="admin-list">
          {users.map((user) => (
            <div key={user.user_id} className="admin-item">
              {editingUser?.user_id === user.user_id ? (
                <div className="edit-form">
                  <h3>Editing User: {user.username}</h3>
                  <div className="edit-fields">
                    {Object.keys(editingUser).map((key) => {
                      // Skip user_id as it shouldn't be edited
                      if (key === "user_id") return null;
                      return renderEditField(
                        key,
                        editingUser[key],
                        (value) =>
                          setEditingUser({
                            ...editingUser,
                            [key]: value,
                          })
                      );
                    })}
                  </div>
                  <div className="button-group">
                    <button className="save-btn" onClick={handleSaveUser}>
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      onClick={() => {
                        setEditingUser(null);
                        setExpandedUser(null);
                      }}
                    >
                      Cancel
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => {
                        setEditingUser(null);
                        setExpandedUser(null);
                        handleDeleteUser(user.user_id);
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ) : (
                <div className="item-summary">
                  <div className="item-info">
                    <strong>ID: {user.user_id}</strong> - {user.username}
                  </div>
                  <div className="item-details">{user.name}</div>
                  <div className="item-details">Role: {user.role}</div>
                  <div className="item-details">
                    Status: {user.is_active ? "Active" : "Inactive"}
                  </div>
                  <div className="summary-buttons">
                    <button
                      className="edit-btn"
                      onClick={() => handleEditUser(user)}
                    >
                      Edit All Attributes
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDeleteUser(user.user_id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AdminPage;