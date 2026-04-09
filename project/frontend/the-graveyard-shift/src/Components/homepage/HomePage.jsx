import { useNavigate } from "react-router-dom";
import "./styles/HomePage.css";

function HomePage() {
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    localStorage.removeItem("userId");
    navigate("/");
    window.location.reload();
  };

  const navigationItems = [
    {
      icon: "🍽️",
      title: "Browse Restaurants",
      description: "Explore menus and discover amazing food",
      link: "/restaurants",
    },
    {
      icon: "🛒",
      title: "My Cart",
      description: "View and manage your shopping cart",
      link: "/cart",
    },
    {
      icon: "📦",
      title: "My Orders",
      description: "Track your current and past orders",
      link: "/orders",
    },
    {
      icon: "⚙️",
      title: "My Profile",
      description: "Manage your account settings",
      link: "/profile",
    },
  ];

  return (
    <div className="homepage-container">
      <header className="homepage-header">
        <div className="header-title">
          <h1>🪦 The Graveyard Shift</h1>
        </div>
        {username && (
          <div className="header-user">
            <div className="user-info">
              <p className="user-username">{username}</p>
              <p className="user-role"> {role?.replace("_", " ").replace(/\b\w/g, c => c.toUpperCase())}</p>
            </div>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </header>

      {!username ? (
        <div className="hero-section">
          <div className="hero-content">
            <h2>Welcome to The Graveyard Shift</h2>
            <p>Your late-night food delivery destination. Order from amazing restaurants anytime.</p>
            <div className="not-logged-in">
              <p>Sign in to get started or create an account</p>
              <div className="auth-buttons">
                <button className="auth-btn login" onClick={() => navigate("/login")}>
                  Sign In
                </button>
                <button className="auth-btn signup" onClick={() => navigate("/signup")}>
                  Create Account
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="welcome-section">
            <div className="welcome-card">
              <h2>Welcome back, {username}!</h2>
              <p>Ready for some late-night food? Browse our restaurants and place an order.</p>
              <div className="quick-actions">
                <a href="/restaurants" className="action-link">
                  🍽️ Browse Restaurants
                </a>
                <a href="/orders" className="action-link">
                  📦 View Orders
                </a>
                {role === "admin" && (
                  <a href="/admin" className="action-link">
                    ⚙️ Admin Panel
                  </a>
                )}
                {role === "restaurant_owner" && (
                  <a href="/restaurant-owner" className="action-link">
                    🏪 Manage Restaurants
                  </a>
                )}
              </div>
            </div>
          </div>

          <div className="navigation-section">
            <h2>Quick Access</h2>
            <div className="nav-grid">
              {navigationItems.map((item) => (
                <a key={item.link} href={item.link} className="nav-card">
                  <div className="nav-card-icon">{item.icon}</div>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                </a>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default HomePage;