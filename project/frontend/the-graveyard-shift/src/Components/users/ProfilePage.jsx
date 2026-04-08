import "./styles/ProfilePage.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function ProfilePage() {
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  useEffect(() => {
    if (!username) return;

    fetch(`http://127.0.0.1:8000/users/${username}`)
      .then((res) => res.json())
      .then((data) => {
        setEmail(data.email || "");
        setPhone(data.phone_number || "");
      })
      .catch((err) => console.error(err));
  }, [username]);

  return (
    <div className="profile-container">
      <header className="profile-header">
        <div className="profile-header-title">
          <h1>👤 My Profile</h1>
          <p>View your account information</p>
        </div>
      </header>

      <main className="profile-content">
        <section className="profile-card">
          <div className="profile-card-top">
            <div className="profile-avatar">👤</div>
            <div className="profile-main-info">
              <h2>{username || "Unknown User"}</h2>
              <p className="profile-role">{role || "No role assigned"}</p>
            </div>
          </div>

          <div className="profile-info-grid">
            <div className="profile-info-item">
              <span className="profile-label">Username</span>
              <span className="profile-value">{username || "-"}</span>
            </div>

            <div className="profile-info-item">
              <span className="profile-label">Role</span>
              <span className="profile-value">{role || "-"}</span>
            </div>

            <div className="profile-info-item">
              <span className="profile-label">Email</span>
              <span className="profile-value">{email || "-"}</span>
            </div>

            <div className="profile-info-item">
              <span className="profile-label">Phone</span>
              <span className="profile-value">{phone || "-"}</span>
            </div>
          </div>

          <div className="profile-actions">
            <button
              className="profile-btn secondary"
              onClick={() => navigate("/")}
            >
              Back to Home
            </button>

            <button
              className="profile-btn primary"
              onClick={() => {
                localStorage.clear();
                navigate("/login");
              }}
            >
              Logout
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ProfilePage;