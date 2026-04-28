import { useState, useCallback } from 'react';
import Navbar      from './components/Navbar';
import HeroSection from './components/HeroSection';
import MenuSection from './components/MenuSection';
import CartDrawer  from './components/CartDrawer';
import Toast       from './components/Toast';
import './index.css';
import './App.css';

export default function App() {
  // ── Cart state ──────────────────────────────────────────
  const [cart, setCart]           = useState([]);
  const [cartOpen, setCartOpen]   = useState(false);

  // ── Toast state ─────────────────────────────────────────
  const [toast, setToast] = useState({ visible: false, message: '', emoji: '✅' });

  const showToast = useCallback((message, emoji = '✅') => {
    setToast({ visible: true, message, emoji });
  }, []);

  const hideToast = useCallback(() => {
    setToast(prev => ({ ...prev, visible: false }));
  }, []);

  // ── Cart handlers ────────────────────────────────────────
  const handleAddToCart = useCallback((item) => {
    setCart(prev => {
      const existing = prev.find(c => c.id === item.id);
      if (existing) {
        return prev.map(c =>
          c.id === item.id ? { ...c, quantity: c.quantity + 1 } : c
        );
      }
      return [...prev, { ...item, quantity: 1 }];
    });
    showToast(`${item.name} added to cart`, '🛒');
  }, [showToast]);

  const handleIncrease = useCallback((id) => {
    setCart(prev =>
      prev.map(c => c.id === id ? { ...c, quantity: c.quantity + 1 } : c)
    );
  }, []);

  const handleDecrease = useCallback((id) => {
    setCart(prev => {
      const item = prev.find(c => c.id === id);
      if (item?.quantity === 1) {
        // Remove if hitting zero
        showToast('Item removed from cart', '🗑️');
        return prev.filter(c => c.id !== id);
      }
      return prev.map(c => c.id === id ? { ...c, quantity: c.quantity - 1 } : c);
    });
  }, [showToast]);

  const handleRemove = useCallback((id) => {
    setCart(prev => {
      const item = prev.find(c => c.id === id);
      if (item) showToast(`${item.name} removed`, '🗑️');
      return prev.filter(c => c.id !== id);
    });
  }, [showToast]);

  const handleClear = useCallback(() => {
    setCart([]);
    showToast('Cart cleared', '🧹');
  }, [showToast]);

  // ── Derived values ───────────────────────────────────────
  const cartCount = cart.reduce((sum, c) => sum + c.quantity, 0);

  return (
    <>
      <Navbar
        cartCount={cartCount}
        onCartOpen={() => setCartOpen(true)}
      />

      <main>
        <HeroSection />
        <MenuSection onAddToCart={handleAddToCart} />
      </main>

      <footer className="footer" id="about">
        <div className="footer__inner">
          <div className="footer__brand-row">
            <span className="footer__brand">🍽️ TiffinBox</span>
            <p className="footer__tagline">Home-cooked meals, delivered with love.</p>
          </div>
          <div className="footer__links">
            <a href="#menu"    className="footer__link">Menu</a>
            <a href="#"        className="footer__link">Privacy</a>
            <a href="#"        className="footer__link">Terms</a>
            <a href="#"        className="footer__link">Contact</a>
          </div>
          <p className="footer__copy">© 2025 TiffinBox. All rights reserved.</p>
        </div>
      </footer>

      {/* Cart drawer + overlay */}
      <CartDrawer
        isOpen={cartOpen}
        onClose={() => setCartOpen(false)}
        cart={cart}
        onIncrease={handleIncrease}
        onDecrease={handleDecrease}
        onRemove={handleRemove}
        onClear={handleClear}
      />

      {/* Toast notification */}
      <Toast
        visible={toast.visible}
        message={toast.message}
        emoji={toast.emoji}
        onHide={hideToast}
      />
    </>
  );
}
