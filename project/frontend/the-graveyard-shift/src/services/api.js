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
};
