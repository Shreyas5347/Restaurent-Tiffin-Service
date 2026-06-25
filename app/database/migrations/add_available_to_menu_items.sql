-- Add available column to menu_items table
ALTER TABLE menu_items ADD COLUMN IF NOT EXISTS available BOOLEAN DEFAULT true;

-- Update existing items to be available by default
UPDATE menu_items SET available = true WHERE available IS NULL;
