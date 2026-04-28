import './HeroSection.css';

export default function HeroSection() {
  return (
    <section className="hero" id="hero">
      {/* Ambient background blobs */}
      <div className="hero__blob hero__blob--1" />
      <div className="hero__blob hero__blob--2" />
      <div className="hero__blob hero__blob--3" />

      <div className="hero__content">
        {/* Badge */}
        <div className="hero__badge">
          <span className="hero__badge-dot" />
          Fresh &amp; Hot — Delivered Daily
        </div>

        {/* Headline */}
        <h1 className="hero__title">
          Home-Cooked <br />
          <span className="hero__title-highlight">Tiffin Service</span>
          <br /> You'll Love
        </h1>

        {/* Subtitle */}
        <p className="hero__subtitle">
          Authentic, nutritious meals prepared fresh every day and delivered
          straight to your doorstep. No preservatives, just real food.
        </p>

        {/* Stats row */}
        <div className="hero__stats">
          <div className="hero__stat">
            <span className="hero__stat-value">500+</span>
            <span className="hero__stat-label">Happy Customers</span>
          </div>
          <div className="hero__stat-divider" />
          <div className="hero__stat">
            <span className="hero__stat-value">30+</span>
            <span className="hero__stat-label">Menu Items</span>
          </div>
          <div className="hero__stat-divider" />
          <div className="hero__stat">
            <span className="hero__stat-value">4.9★</span>
            <span className="hero__stat-label">Average Rating</span>
          </div>
        </div>

        {/* CTAs */}
        <div className="hero__ctas">
          <a href="#menu" className="hero__cta hero__cta--primary" id="explore-menu-btn">
            Explore Menu
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12,5 19,12 12,19"/>
            </svg>
          </a>
          <a href="#about" className="hero__cta hero__cta--ghost" id="learn-more-btn">
            Learn More
          </a>
        </div>
      </div>

      {/* Decorative food emojis floating */}
      <div className="hero__floats" aria-hidden="true">
        <span className="hero__float hero__float--1">🍛</span>
        <span className="hero__float hero__float--2">🥘</span>
        <span className="hero__float hero__float--3">🍱</span>
        <span className="hero__float hero__float--4">🫓</span>
        <span className="hero__float hero__float--5">🍵</span>
      </div>
    </section>
  );
}
