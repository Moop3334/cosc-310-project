function HomePage() {
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    window.location.reload();
  };

  return (
    <div>
      <h1>Welcome {username}</h1>
      <p>Role: {role}</p>

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default HomePage;