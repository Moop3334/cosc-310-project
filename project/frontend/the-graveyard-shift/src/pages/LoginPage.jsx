import { useState } from "react";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [passwordHash, setPasswordHash] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch("http://localhost:8000/users/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password_hash: passwordHash,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Login failed");
      return;
    }

    localStorage.setItem("username", username);

    const userResponse = await fetch(`http://localhost:8000/users/${username}`);
    const userData = await userResponse.json();

    if (!userResponse.ok) {
      setMessage("Login worked, but failed to get user info");
      return;
    }

    localStorage.setItem("role", userData.role || "");
    setMessage(`Welcome ${userData.username} (${userData.role})`);
  } catch (error) {
    setMessage("Could not connect to backend");
  }
};

  return (
    <div>
      <h1>Login Page</h1>

      <form onSubmit={handleLogin}>
        <div>
          <label>Username: </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div>
          <label>Password: </label>
          <input
            type="password"
            value={passwordHash}
            onChange={(e) => setPasswordHash(e.target.value)}
          />
        </div>

        <button type="submit">Log In</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default LoginPage;