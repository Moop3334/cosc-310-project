import RestaurantBrowser from './components/restaurants/RestaurantBrowser'
import RestaurantOwnerDashboard from './components/restaurants/RestaurantOwnerDashboard'
import Cart from './components/checkout/Cart'
import CheckoutPage from './components/checkout/CheckoutPage'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./components/users/LoginPage";
import SignupPage from "./components/users/SignupPage";
import HomePage from "./components/homepage/HomePage";
import AdminPage from "./components/admin/AdminPage";
import OrdersPage from "./components/orders/OrdersPage";
import ProtectedRoute from "./components/ProtectedRoute";
import UserRoute from './components/UserRoute';
import ProfilePage from "./components/users/ProfilePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />

        <Route 
          path="/restaurants" 
          element={
            <UserRoute>
              <RestaurantBrowser />
            </UserRoute>
          } 
        />
        <Route 
          path="/orders" 
          element={
            <UserRoute>
              <OrdersPage />
            </UserRoute>
          } 
        />
        <Route 
          path="/cart" 
          element={
            <UserRoute>
              <Cart />
            </UserRoute>
          } 
        />
        <Route 
          path="/checkout" 
          element={
            <UserRoute>
              <CheckoutPage />
            </UserRoute>
          } 
        />

        <Route
          path="/restaurant-owner"
          element={
            <ProtectedRoute requiredRole="restaurant_owner">
              <RestaurantOwnerDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <ProtectedRoute requiredRole="admin">
              <AdminPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;