-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id   SERIAL PRIMARY KEY,
    key  VARCHAR(50)  UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(10)  DEFAULT '🍽️',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Seed the 4 default categories (skip if already present)
INSERT INTO categories (key, name, icon) VALUES
    ('tiffin', 'Tiffin Combos', '🍱'),
    ('sabzi',  'Sabzi & Curry', '🍛'),
    ('rice',   'Rice & Roti',   '🍚'),
    ('snacks', 'Snacks',        '🥣')
ON CONFLICT (key) DO NOTHING;
