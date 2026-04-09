import { useState, useEffect } from "react";

function AdminPage() {
  const [role, setRole] = useState(localStorage.getItem("role"));
  const [restaurants, setRestaurants] = useState([]);
  const [orders, setOrders] = useState([]);
  const [editingRestaurant, setEditingRestaurant] = useState(null);
  const [editingOrder, setEditingOrder] = useState(null);

  useEffect(() => {
    if (role === "admin") {
      fetchRestaurants();
      fetchOrders();
    }
  }, [role]);

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

  const handleEditRestaurant = (restaurant) => {
    setEditingRestaurant(restaurant);
  };

  const handleSaveRestaurant = async () => {
    try {
      await fetch(`/api/restaurants/${editingRestaurant.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingRestaurant),
      });
      setEditingRestaurant(null);
      fetchRestaurants();
    } catch (error) {
      console.error("Error saving restaurant:", error);
    }
  };

  const handleEditOrder = (order) => {
    setEditingOrder(order);
  };

  const handleSaveOrder = async () => {
    try {
      await fetch(`/api/orders/${editingOrder.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingOrder),
      });
      setEditingOrder(null);
      fetchOrders();
    } catch (error) {
      console.error("Error saving order:", error);
    }
  };

  if (role !== "admin") {
    return (
      <div>
        <h1>Access Denied</h1>
        <p>You do not have admin privileges.</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Only admins can see this page.</p>

      <h2>Restaurants</h2>
      <ul>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>
            {editingRestaurant?.id === restaurant.id ? (
              <div>
                <input
                  value={editingRestaurant.name}
                  onChange={(e) =>
                    setEditingRestaurant({ ...editingRestaurant, name: e.target.value })
                  }
                />
                <button onClick={handleSaveRestaurant}>Save</button>
                <button onClick={() => setEditingRestaurant(null)}>Cancel</button>
              </div>
            ) : (
              <div>
                {restaurant.name}
                <button onClick={() => handleEditRestaurant(restaurant)}>Edit</button>
              </div>
            )}
          </li>
        ))}
      </ul>

      <h2>Orders</h2>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            {editingOrder?.id === order.id ? (
              <div>
                <input
                  value={editingOrder.status}
                  onChange={(e) =>
                    setEditingOrder({ ...editingOrder, status: e.target.value })
                  }
                />
                <button onClick={handleSaveOrder}>Save</button>
                <button onClick={() => setEditingOrder(null)}>Cancel</button>
              </div>
            ) : (
              <div>
                Order ID: {order.id}, Status: {order.status}
                <button onClick={() => handleEditOrder(order)}>Edit</button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPage;