import { useEffect } from 'react';
import './CartDrawer.css';

// Category → emoji mapping (same as MenuCard)
const categoryEmoji = {
  Breakfast: '🌅', Lunch: '🍱', Dinner: '🍛',
  Snacks: '🥪', Beverages: '☕', Desserts: '🍮',
  Uncategorized: '🍽️',
};

const DELIVERY_FEE = 30;
const FREE_DELIVERY_THRESHOLD = 300;
const GST_RATE = 0.05; // 5%

function CartItem({ item, onIncrease, onDecrease, onRemove }) {
  const emoji = categoryEmoji[item.category] || '🍽️';
  const lineTotal = (item.price * item.quantity).toFixed(2);

  return (
    <div className="cart-item" id={`cart-item-${item.id}`}>
      {/* Emoji thumbnail */}
      <div className="cart-item__emoji" aria-hidden="true">{emoji}</div>

      {/* Name + unit price */}
      <div className="cart-item__info">
        <p className="cart-item__name">{item.name}</p>
        <p className="cart-item__unit-price">₹{item.price.toFixed(2)} each</p>
      </div>

      {/* Right side — qty + total + remove */}
      <div className="cart-item__controls">
        {/* Quantity stepper */}
        <div className="cart-item__qty">
          <button
            className="cart-item__qty-btn"
            id={`qty-decrease-${item.id}`}
            onClick={() => onDecrease(item.id)}
            aria-label="Decrease quantity"
          >
            −
          </button>
          <span className="cart-item__qty-value">{item.quantity}</span>
          <button
            className="cart-item__qty-btn"
            id={`qty-increase-${item.id}`}
            onClick={() => onIncrease(item.id)}
            aria-label="Increase quantity"
          >
            +
          </button>
        </div>

        <span className="cart-item__total">₹{lineTotal}</span>

        <button
          className="cart-item__remove"
          id={`remove-item-${item.id}`}
          onClick={() => onRemove(item.id)}
          aria-label={`Remove ${item.name}`}
        >
          Remove
        </button>
      </div>
    </div>
  );
}

export default function CartDrawer({ isOpen, onClose, cart, onIncrease, onDecrease, onRemove, onClear }) {
  const itemCount  = cart.reduce((s, c) => s + c.quantity, 0);
  const subtotal   = cart.reduce((s, c) => s + c.price * c.quantity, 0);
  const isFreeDelivery = subtotal >= FREE_DELIVERY_THRESHOLD;
  const deliveryFee    = isFreeDelivery ? 0 : DELIVERY_FEE;
  const gst            = subtotal * GST_RATE;
  const total          = subtotal + deliveryFee + gst;

  // Lock body scroll when drawer is open
  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  // Close on Escape key
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [isOpen, onClose]);

  return (
    <>
      {/* Backdrop */}
      <div
        className={`cart-overlay ${isOpen ? 'cart-overlay--visible' : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <aside
        className={`cart-drawer ${isOpen ? 'cart-drawer--open' : ''}`}
        aria-label="Shopping cart"
        role="dialog"
        aria-modal="true"
      >
        {/* ── Header ── */}
        <div className="cart-drawer__header">
          <div className="cart-drawer__title">
            <h2>Your Cart</h2>
            {itemCount > 0 && (
              <span className="cart-drawer__count-badge">
                {itemCount} {itemCount === 1 ? 'item' : 'items'}
              </span>
            )}
          </div>
          <button
            className="cart-drawer__close"
            id="cart-close-btn"
            onClick={onClose}
            aria-label="Close cart"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6"  y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        {/* ── Body ── */}
        <div className="cart-drawer__body">
          {cart.length === 0 ? (
            <div className="cart-empty">
              <span className="cart-empty__icon">🛒</span>
              <h3 className="cart-empty__title">Your cart is empty</h3>
              <p className="cart-empty__subtitle">
                Looks like you haven't added anything yet. Explore our menu and find something delicious!
              </p>
              <a
                href="#menu"
                className="cart-empty__cta"
                id="browse-menu-btn"
                onClick={onClose}
              >
                Browse Menu
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12,5 19,12 12,19"/>
                </svg>
              </a>
            </div>
          ) : (
            <>
              {/* Free delivery progress */}
              {!isFreeDelivery && (
                <div className="cart-delivery-strip">
                  🚀 Add ₹{(FREE_DELIVERY_THRESHOLD - subtotal).toFixed(0)} more for FREE delivery!
                </div>
              )}
              {isFreeDelivery && (
                <div className="cart-delivery-strip">
                  🎉 You've unlocked FREE delivery!
                </div>
              )}

              {/* Item list */}
              {cart.map(item => (
                <CartItem
                  key={item.id}
                  item={item}
                  onIncrease={onIncrease}
                  onDecrease={onDecrease}
                  onRemove={onRemove}
                />
              ))}
            </>
          )}
        </div>

        {/* ── Footer / Summary ── */}
        {cart.length > 0 && (
          <div className="cart-drawer__footer">
            <div className="cart-summary">
              <div className="cart-summary__row">
                <span>Subtotal</span>
                <span className="cart-summary__amount">₹{subtotal.toFixed(2)}</span>
              </div>
              <div className="cart-summary__row">
                <span>GST (5%)</span>
                <span className="cart-summary__amount">₹{gst.toFixed(2)}</span>
              </div>
              <div className="cart-summary__row">
                <span>Delivery</span>
                <span className="cart-summary__amount">
                  {isFreeDelivery
                    ? <span className="cart-summary__label-free">FREE</span>
                    : `₹${deliveryFee.toFixed(2)}`
                  }
                </span>
              </div>
              <div className="cart-summary__row cart-summary__row--total">
                <span>Total</span>
                <span className="cart-summary__amount">₹{total.toFixed(2)}</span>
              </div>
            </div>

            <div className="cart-drawer__actions">
              <button
                className="cart-drawer__place-btn"
                id="place-order-btn"
                disabled={cart.length === 0}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M20 12V22H4V12"/><path d="M22 7H2v5h20V7z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>
                </svg>
                Place Order · ₹{total.toFixed(2)}
              </button>

              <button
                className="cart-drawer__clear-btn"
                id="clear-cart-btn"
                onClick={onClear}
              >
                Clear Cart
              </button>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}
