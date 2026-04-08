import RestaurantBrowser from './components/restaurants/RestaurantBrowser'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./components/users/LoginPage";
import SignupPage from "./components/users/SignupPage";
import HomePage from "./components/homepage/HomePage";
import AdminPage from "./components/admin/AdminPage";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/restaurants" element={<RestaurantBrowser />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

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