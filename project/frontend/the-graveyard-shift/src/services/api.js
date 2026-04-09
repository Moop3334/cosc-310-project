// Use /api prefix which will be proxied by Vite dev server
// In production, this will need to be handled by nginx or similar
const API_BASE_URL = '/api';

export const restaurantAPI = {
  // Get all restaurants or search by name
  getRestaurants: async (name = null) => {
    try {
      const url = name
        ? `${API_BASE_URL}/restaurants?name=${encodeURIComponent(name)}`
        : `${API_BASE_URL}/restaurants`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch restaurants');
      return await response.json();
    } catch (error) {
      console.error('Error fetching restaurants:', error);
      throw error;
    }
  },

  // Get a specific restaurant by ID
  getRestaurantById: async (restaurantId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}`);
      if (!response.ok) throw new Error('Failed to fetch restaurant');
      return await response.json();
    } catch (error) {
      console.error('Error fetching restaurant:', error);
      throw error;
    }
  },

  // Get menu for a restaurant
  getMenu: async (restaurantId, name = null) => {
    try {
      const url = name
        ? `${API_BASE_URL}/restaurants/${restaurantId}/menu?name=${encodeURIComponent(name)}`
        : `${API_BASE_URL}/restaurants/${restaurantId}/menu`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch menu');
      return await response.json();
    } catch (error) {
      console.error('Error fetching menu:', error);
      throw error;
    }
  },

  // Get a specific menu item
  getMenuItemById: async (restaurantId, itemId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}/menu/${itemId}`);
      if (!response.ok) throw new Error('Failed to fetch menu item');
      return await response.json();
    } catch (error) {
      console.error('Error fetching menu item:', error);
      throw error;
    }
  },

  // Create a new restaurant
  createRestaurant: async (restaurantData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(restaurantData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create restaurant');
      }
      return await response.json();
    } catch (error) {
      console.error('Error creating restaurant:', error);
      throw error;
    }
  },

  // Update an existing restaurant
  updateRestaurant: async (restaurantId, restaurantData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(restaurantData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update restaurant');
      }
      return await response.json();
    } catch (error) {
      console.error('Error updating restaurant:', error);
      throw error;
    }
  },

  // Delete a restaurant
  deleteRestaurant: async (restaurantId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete restaurant');
      }
      return true;
    } catch (error) {
      console.error('Error deleting restaurant:', error);
      throw error;
    }
  },
};

export const orderAPI = {
  // Get all orders
  getOrders: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/orders`);
      if (!response.ok) throw new Error('Failed to fetch orders');
      return await response.json();
    } catch (error) {
      console.error('Error fetching orders:', error);
      throw error;
    }
  },
};

export const recommendationAPI = {
  // Get recommendations for a user
  getRecommendations: async (userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/recommendations/${userId}`);
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch recommendations');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      throw error;
    }
  },
};

export const userAPI = {
  // Get user by username
  getUserByUsername: async (username) => {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${username}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return await response.json();
    } catch (error) {
      console.error('Error fetching user:', error);
      throw error;
    }
  },

  // Update user
  updateUser: async (username, userData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${username}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      if (!response.ok) throw new Error('Failed to update user');
      return await response.json();
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  },
};

export const cartAPI = {
  // Add item to cart
  addToCart: async (userId, restaurantId, item) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}/add?restaurant_id=${restaurantId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to add item to cart');
      }
      return await response.json();
    } catch (error) {
      console.error('Error adding item to cart:', error);
      throw error;
    }
  },

  // Get cart for user
  getCart: async (userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch cart');
      return await response.json();
    } catch (error) {
      console.error('Error fetching cart:', error);
      throw error;
    }
  },

  // Remove one of an item from cart
  removeItem: async (userId, itemId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}/items/${itemId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to remove item from cart');
      }
      return await response.json();
    } catch (error) {
      console.error('Error removing item from cart:', error);
      throw error;
    }
  },

  // Remove all of an item from cart
  removeAllItems: async (userId, itemId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}/items/${itemId}/clear`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to remove all items from cart');
      }
      return await response.json();
    } catch (error) {
      console.error('Error removing all items from cart:', error);
      throw error;
    }
  },

  // Clear entire cart
  clearCart: async (userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}/clear`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to clear cart');
      }
      return await response.json();
    } catch (error) {
      console.error('Error clearing cart:', error);
      throw error;
    }
  },

  // Get cart summary with pricing breakdown
  getCartSummary: async (userId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/cart/${userId}/summary`);
      if (!response.ok) throw new Error('Failed to fetch cart summary');
      return await response.json();
    } catch (error) {
      console.error('Error fetching cart summary:', error);
      throw error;
    }
  },
};