import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, requiredRole }) {
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  if (!username) {
    return <Navigate to="/login" />;
  }

  if (requiredRole && role !== requiredRole) {
    return <Navigate to="/" />;
  }

  return children;
}

export default ProtectedRoute;