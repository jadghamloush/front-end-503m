import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Profile = ({ setIsLoggedIn }) => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  // Fetch the user's profile information on component mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get("http://localhost:5000/profile", {
          withCredentials: true,
        });
        setUsername(response.data.username);
      } catch (error) {
        console.error("Error fetching profile:", error);
        // If not authenticated, redirect to login
        navigate("/login");
      }
    };

    fetchProfile();
  }, [navigate]);

  // Handle logout and redirect to login page
  const handleLogout = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/logout",
        {},
        { withCredentials: true }
      );
      if (response.data.message === "Logged out successfully") {
        setIsLoggedIn(false);
        navigate("/login");
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Welcome, {username}!</h1>
      <button onClick={handleLogout} style={styles.logoutButton}>
        Log Out
      </button>
    </div>
  );
};

export default Profile;

// Inline styles for simplicity
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#f0f2f5",
  },
  logoutButton: {
    padding: "10px 20px",
    marginTop: "20px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "1rem",
  },
};
