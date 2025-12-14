import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { sweetsAPI, authAPI, Sweet } from "../api";
import SweetCard from "../components/SweetCard";
import AddSweetModal from "../components/AddSweetModal";
import "./Dashboard.css";

export default function Dashboard() {
  const [user, setUser] = useState<any>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    // Get current user info from API
    authAPI.getMe()
      .then((userData) => {
        setUser(userData);
        setIsAdmin(userData.role === "admin");
      })
      .catch((err) => {
        console.error("Failed to get user info", err);
        // If token is invalid, redirect to login
        if (err.response?.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
        }
      });
  }, [navigate]);

  const { data: sweets = [], isLoading } = useQuery({
    queryKey: ["sweets"],
    queryFn: sweetsAPI.getAll,
  });

  const purchaseMutation = useMutation({
    mutationFn: sweetsAPI.purchase,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sweets"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: sweetsAPI.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sweets"] });
    },
  });

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handlePurchase = (id: number) => {
    purchaseMutation.mutate(id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm("Are you sure you want to delete this sweet?")) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Sweet Shop Management System</h1>
        <div className="header-actions">
          {isAdmin && (
            <button
              className="btn-primary"
              onClick={() => setShowAddModal(true)}
            >
              Add Sweet
            </button>
          )}
          <button className="btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        {isLoading ? (
          <div className="loading">Loading sweets...</div>
        ) : sweets.length === 0 ? (
          <div className="empty-state">
            <p>
              No sweets available.{" "}
              {isAdmin && "Add some sweets to get started!"}
            </p>
          </div>
        ) : (
          <div className="sweets-grid">
            {sweets.map((sweet: Sweet) => (
              <SweetCard
                key={sweet.id}
                sweet={sweet}
                onPurchase={handlePurchase}
                onDelete={handleDelete}
                isPurchasing={purchaseMutation.isPending}
                isAdmin={isAdmin}
              />
            ))}
          </div>
        )}
      </main>

      {showAddModal && (
        <AddSweetModal
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            queryClient.invalidateQueries({ queryKey: ["sweets"] });
          }}
        />
      )}
    </div>
  );
}
