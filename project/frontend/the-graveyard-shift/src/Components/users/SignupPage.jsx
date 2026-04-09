import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/SignupPage.css";

function SignupPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    username: "",
    phone_number: "",
    address: "",
    password_hash: "",
    confirmPassword: "",
    role: "customer",
    credit:5,
  });

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    // Validation
    if (formData.password_hash !== formData.confirmPassword) {
      setMessage("Passwords do not match.");
      setMessageType("error");
      setLoading(false);
      return;
    }

    if (formData.password_hash.length < 6) {
      setMessage("Password must be at least 6 characters long.");
      setMessageType("error");
      setLoading(false);
      return;
    }

    try {
      const signupUrl = `/api/users/signup`;
      console.log("Full signup URL:", signupUrl);
      
      const res = await fetch(signupUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.name,
          phone_number: formData.phone_number,
          address: formData.address,
          username: formData.username,
          email: formData.email,
          password_hash: formData.password_hash,
          role: formData.role,
          credit:5,
        }),
      });

      console.log("Response status:", res.status);
      const data = await res.json();
      console.log("Response data:", data);

      if (!res.ok) {
        setMessage(data.detail || "Signup failed. Please try again.");
        setMessageType("error");
        return;
      }

      setMessage("Account created successfully! Redirecting to login...");
      setMessageType("success");

      // Redirect to login after success
      setTimeout(() => {
        navigate("/login");
      }, 1500);
    } catch (error) {
      console.error("Signup error:", error);
      setMessage(`Error: ${error.message}`);
      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-header">
        <h1>🪦 Join The Graveyard Shift</h1>
        <p>Create your account to get started</p>
      </div>

      <div className="signup-content">
        <div className="signup-card">
          <form className="signup-form" onSubmit={handleSignup}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">Full Name</label>
                <input
                  id="name"
                  type="text"
                  name="name"
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  id="username"
                  type="text"
                  name="username"
                  placeholder="johndoe"
                  value={formData.username}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="john@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  id="phone"
                  type="tel"
                  name="phone_number"
                  placeholder="(555) 123-4567"
                  value={formData.phone_number}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="address">Address</label>
              <input
                id="address"
                type="text"
                name="address"
                placeholder="123 Main St, City, State 12345"
                value={formData.address}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  name="password_hash"
                  placeholder="At least 6 characters"
                  value={formData.password_hash}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  id="confirmPassword"
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="role">Account Type</label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                disabled={loading}
                required
              >
                <option value="customer">Customer</option>
                <option value="driver">Delivery Driver</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <button
              type="submit"
              className={`signup-button ${loading ? "loading" : ""}`}
              disabled={loading}
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          {message && <div className={`message ${messageType}`}>{message}</div>}

          <div className="login-link">
            Already have an account? <a href="/login">Sign in here</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;