import { Sweet } from "../api";
import "./SweetCard.css";

interface SweetCardProps {
  sweet: Sweet;
  onPurchase: (id: number) => void;
  onDelete?: (id: number) => void;
  isPurchasing: boolean;
  isAdmin?: boolean;
}

export default function SweetCard({
  sweet,
  onPurchase,
  onDelete,
  isPurchasing,
  isAdmin = false,
}: SweetCardProps) {
  return (
    <div className="sweet-card">
      <div className="sweet-header">
        <h3>{sweet.name}</h3>
        <span className="category">{sweet.category}</span>
      </div>
      <div className="sweet-details">
        <div className="price">${sweet.price.toFixed(2)}</div>
        <div className="quantity">
          {sweet.quantity > 0 ? (
            <span className="in-stock">{sweet.quantity} in stock</span>
          ) : (
            <span className="out-of-stock">Out of stock</span>
          )}
        </div>
      </div>
      <div className="sweet-actions">
        <button
          className="purchase-btn"
          onClick={() => onPurchase(sweet.id)}
          disabled={sweet.quantity === 0 || isPurchasing}
        >
          {isPurchasing ? "Purchasing..." : "Buy Now"}
        </button>
        {isAdmin && onDelete && (
          <button
            className="delete-btn"
            onClick={() => onDelete(sweet.id)}
            title="Delete sweet"
          >
            🗑️ Delete
          </button>
        )}
      </div>
    </div>
  );
}
