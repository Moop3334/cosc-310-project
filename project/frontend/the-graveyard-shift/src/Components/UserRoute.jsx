import { Navigate } from "react-router-dom";

function UserRoute({ children }) {
  const username = localStorage.getItem("username");

  if (!username) {
    return <Navigate to="/login" />;
  }

  return children;
}

export default UserRoute;