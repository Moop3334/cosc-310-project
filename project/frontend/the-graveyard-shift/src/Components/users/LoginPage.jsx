import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/LoginPage.css";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [passwordHash, setPasswordHash] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const loginUrl = `/api/users/login`;
      console.log("Full login URL:", loginUrl);
      
      const response = await fetch(loginUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password_hash: passwordHash,
        }),
      });

      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);

      if (!response.ok) {
        setMessage(data.detail || "Login failed. Please check your credentials.");
        setMessageType("error");
        return;
      }

      localStorage.setItem("username", username);

      const userUrl = `/api/users/${username}`;
      const userResponse = await fetch(userUrl);
      const userData = await userResponse.json();

      if (!userResponse.ok) {
        setMessage("Login successful, but failed to retrieve user info. Please try again.");
        setMessageType("error");
        return;
      }

      localStorage.setItem("role", userData.role || "customer");
      // Store userId - use id field, fallback to username if id is not available
      const userId = userData.id || userData.user_id || username;
      localStorage.setItem("userId", String(userId).trim());
      
      console.log('Login successful - stored userId:', userId, 'username:', username);
      
      setMessage(`Welcome back, ${userData.username}!`);
      setMessageType("success");
      
      // Redirect after successful login
      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (error) {
      console.error("Login error:", error);
      setMessage(`Error: ${error.message}`);
      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        <h1>🪦 Welcome Back</h1>
        <p>Sign in to The Graveyard Shift</p>
      </div>

      <div className="login-content">
        <div className="login-card">
          <form className="login-form" onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={passwordHash}
                onChange={(e) => setPasswordHash(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            <button 
              type="submit" 
              className={`login-button ${loading ? "loading" : ""}`}
              disabled={loading}
            >
              {loading ? "Logging in..." : "Log In"}
            </button>
          </form>

          {message && <div className={`message ${messageType}`}>{message}</div>}

          <div className="signup-link">
            Don't have an account? <a href="/signup">Create one here</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;