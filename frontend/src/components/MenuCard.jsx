import './MenuCard.css';

// Category emoji mapping
const categoryEmoji = {
  'Breakfast': '🌅',
  'Lunch': '🍱',
  'Dinner': '🍛',
  'Snacks': '🥪',
  'Beverages': '☕',
  'Desserts': '🍮',
  'Uncategorized': '🍽️',
};

export default function MenuCard({ item, onAddToCart }) {
  const emoji = categoryEmoji[item.category] || '🍽️';

  return (
    <div className="menu-card" id={`menu-item-${item.id}`}>
      {/* Card header - decorative placeholder image */}
      <div className="menu-card__image">
        <span className="menu-card__emoji">{emoji}</span>
        <span className="menu-card__category-badge">{item.category}</span>
      </div>

      {/* Card body */}
      <div className="menu-card__body">
        <h3 className="menu-card__name">{item.name}</h3>
        <p className="menu-card__description">
          {item.description || 'A delicious item crafted with fresh ingredients.'}
        </p>

        <div className="menu-card__footer">
          <div className="menu-card__price">
            <span className="menu-card__price-currency">₹</span>
            <span className="menu-card__price-value">{item.price.toFixed(2)}</span>
          </div>
          <button
            className="menu-card__add-btn"
            id={`add-to-cart-${item.id}`}
            onClick={() => onAddToCart(item)}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Add
          </button>
        </div>
      </div>
    </div>
  );
}
