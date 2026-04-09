import { Navigate } from "react-router-dom";
import NotificationBell from "./notifications/NotificationBell";

function UserRoute({ children }) {
  const username = localStorage.getItem("username");

  if (!username) {
    return <Navigate to="/login" />;
  }

  return (
    <>
      <NotificationBell />
      {children}
    </>
  );
}

export default UserRoute;