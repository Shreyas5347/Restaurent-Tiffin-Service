import { useState, useEffect } from 'react';
import { fetchMenuItems } from '../services/api';
import MenuCard from './MenuCard';
import './MenuSection.css';

// All unique categories derived from items
function getCategories(items) {
  const cats = ['All', ...new Set(items.map(i => i.category))];
  return cats;
}

// Skeleton placeholder cards while loading
function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-card__img" />
      <div className="skeleton-card__body">
        <div className="skeleton skeleton-card__title" />
        <div className="skeleton skeleton-card__desc" />
        <div className="skeleton skeleton-card__desc skeleton-card__desc--short" />
        <div className="skeleton-card__footer">
          <div className="skeleton skeleton-card__price" />
          <div className="skeleton skeleton-card__btn" />
        </div>
      </div>
    </div>
  );
}

export default function MenuSection({ onAddToCart }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState('All');
  const [search, setSearch] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchMenuItems()
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const categories = getCategories(items);

  const filtered = items.filter(item => {
    const matchCat = activeCategory === 'All' || item.category === activeCategory;
    const matchSearch = item.name.toLowerCase().includes(search.toLowerCase());
    return matchCat && matchSearch;
  });

  return (
    <section className="menu-section" id="menu">
      <div className="menu-section__inner">

        {/* Section header */}
        <div className="menu-section__header">
          <span className="menu-section__label">What We Offer</span>
          <h2 className="menu-section__title">Our <span className="menu-section__title-accent">Menu</span></h2>
          <p className="menu-section__subtitle">
            Browse through our freshly prepared dishes, made with love and the finest ingredients.
          </p>
        </div>

        {/* Search bar */}
        <div className="menu-section__search-wrap">
          <svg className="menu-section__search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            id="menu-search-input"
            type="text"
            className="menu-section__search"
            placeholder="Search dishes..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        {/* Category filter tabs */}
        {!loading && !error && (
          <div className="menu-section__tabs" role="tablist">
            {categories.map(cat => (
              <button
                key={cat}
                id={`tab-${cat.toLowerCase()}`}
                role="tab"
                aria-selected={activeCategory === cat}
                className={`menu-section__tab ${activeCategory === cat ? 'menu-section__tab--active' : ''}`}
                onClick={() => setActiveCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        )}

        {/* States */}
        {loading && (
          <div className="menu-section__grid">
            {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        )}

        {error && (
          <div className="menu-section__error">
            <span className="menu-section__error-icon">⚠️</span>
            <p>Could not load menu. Make sure the backend is running.</p>
            <code>{error}</code>
          </div>
        )}

        {!loading && !error && filtered.length === 0 && (
          <div className="menu-section__empty">
            <span>🔍</span>
            <p>No dishes found for "<strong>{search}</strong>"</p>
          </div>
        )}

        {!loading && !error && filtered.length > 0 && (
          <div className="menu-section__grid">
            {filtered.map((item, idx) => (
              <div key={item.id} style={{ animationDelay: `${idx * 0.05}s` }}>
                <MenuCard item={item} onAddToCart={onAddToCart} />
              </div>
            ))}
          </div>
        )}

        {/* Item count */}
        {!loading && !error && (
          <p className="menu-section__count">
            Showing <strong>{filtered.length}</strong> of <strong>{items.length}</strong> items
          </p>
        )}
      </div>
    </section>
  );
}
