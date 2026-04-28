import { useState, useEffect } from 'react';
import './Navbar.css';

export default function Navbar({ cartCount = 0, onCartOpen }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu on resize to desktop
  useEffect(() => {
    const handleResize = () => { if (window.innerWidth > 768) setMenuOpen(false); };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`}>
      <div className="navbar__inner">
        {/* Logo */}
        <a href="/" className="navbar__logo">
          <span className="navbar__logo-icon">🍽️</span>
          <span className="navbar__logo-text">
            Tiffin<span className="navbar__logo-accent">Box</span>
          </span>
        </a>

        {/* Desktop nav links */}
        <div className="navbar__links">
          <a href="#hero"  className="navbar__link">Home</a>
          <a href="#menu"  className="navbar__link">Menu</a>
          <a href="#about" className="navbar__link">About</a>
        </div>

        {/* Actions */}
        <div className="navbar__actions">
          <button className="btn btn--ghost" id="login-btn">Login</button>

          <button className="btn btn--primary" id="cart-btn" onClick={onCartOpen}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            Cart
            {cartCount > 0 && (
              <span className="navbar__cart-badge">{cartCount}</span>
            )}
          </button>

          {/* Mobile hamburger */}
          <button
            className={`navbar__hamburger ${menuOpen ? 'navbar__hamburger--open' : ''}`}
            id="hamburger-btn"
            aria-label="Toggle menu"
            onClick={() => setMenuOpen(prev => !prev)}
          >
            <span /><span /><span />
          </button>
        </div>
      </div>

      {/* Mobile dropdown */}
      <div className={`navbar__mobile-menu ${menuOpen ? 'navbar__mobile-menu--open' : ''}`}>
        <a href="#hero"  className="navbar__mobile-link" onClick={() => setMenuOpen(false)}>Home</a>
        <a href="#menu"  className="navbar__mobile-link" onClick={() => setMenuOpen(false)}>Menu</a>
        <a href="#about" className="navbar__mobile-link" onClick={() => setMenuOpen(false)}>About</a>
        <button className="btn btn--ghost navbar__mobile-login" id="mobile-login-btn">Login</button>
      </div>
    </nav>
  );
}
