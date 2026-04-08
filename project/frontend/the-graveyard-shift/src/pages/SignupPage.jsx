import { useState } from "react";

function SignupPage() {
  const [message, setMessage] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/users/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: "test",
          phone_number: "123",
          address: "test",
          username: "newuser",
          email: "test@test.com",
          password_hash: "123",
          role: "customer",
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.detail);
        return;
      }

      setMessage("Signup success");
    } catch {
      setMessage("Error");
    }
  };

  return (
    <div>
      <h1>Signup</h1>
      <button onClick={handleSignup}>Create Test User</button>
      <p>{message}</p>
    </div>
  );
}

export default SignupPage;