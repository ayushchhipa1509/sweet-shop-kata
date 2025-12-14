import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { authAPI, sweetsAPI, User } from "../api";
import "./Profile.css";

export default function Profile() {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    // Get current user info
    authAPI
      .getMe()
      .then((userData) => {
        setUser(userData);
      })
      .catch((err) => {
        console.error("Failed to get user info", err);
        if (err.response?.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
        }
      });
  }, [navigate]);

  // Get sweets count for admin stats
  const { data: sweets = [] } = useQuery({
    queryKey: ["sweets"],
    queryFn: sweetsAPI.getAll,
    enabled: user?.role === "admin", // Only fetch if admin
  });

  const handleBackToDashboard = () => {
    navigate("/dashboard");
  };

  if (!user) {
    return (
      <div className="profile-container">
        <div className="loading">Loading profile...</div>
      </div>
    );
  }

  const isAdmin = user.role === "admin";
  const totalSweets = sweets.length;
  const totalInStock = sweets.reduce((sum, sweet) => sum + sweet.quantity, 0);
  const outOfStock = sweets.filter((sweet) => sweet.quantity === 0).length;

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>User Profile</h1>
        <button className="btn-secondary" onClick={handleBackToDashboard}>
          Back to Dashboard
        </button>
      </div>

      <div className="profile-content">
        <div className="profile-card">
          <div className="profile-avatar">
            <div className="avatar-circle">
              {user.username.charAt(0).toUpperCase()}
            </div>
            {isAdmin && <span className="admin-badge">Admin</span>}
          </div>

          <div className="profile-info">
            <h2>{user.username}</h2>
            <div className="info-section">
              <div className="info-item">
                <span className="info-label">Email:</span>
                <span className="info-value">{user.email}</span>
              </div>
              <div className="info-item">
                <span className="info-label">User ID:</span>
                <span className="info-value">#{user.id}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Role:</span>
                <span className={`info-value role-badge ${user.role}`}>
                  {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {isAdmin && (
          <div className="admin-section">
            <h3>Admin Dashboard</h3>
            <div className="admin-stats">
              <div className="stat-card">
                <div className="stat-value">{totalSweets}</div>
                <div className="stat-label">Total Sweets</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{totalInStock}</div>
                <div className="stat-label">Items in Stock</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{outOfStock}</div>
                <div className="stat-label">Out of Stock</div>
              </div>
            </div>
            <div className="admin-permissions">
              <h4>Admin Permissions</h4>
              <ul>
                <li>✓ Create new sweets</li>
                <li>✓ Delete sweets</li>
                <li>✓ View all inventory statistics</li>
                <li>✓ Manage shop inventory</li>
              </ul>
            </div>
          </div>
        )}

        {!isAdmin && (
          <div className="user-section">
            <h3>User Permissions</h3>
            <ul>
              <li>✓ View all sweets</li>
              <li>✓ Purchase sweets</li>
              <li>✓ Create new sweets</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
