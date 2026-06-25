-- Add customer_name column to orders table
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);

-- Update order status enum to include new statuses
-- Note: PostgreSQL doesn't have ENUM by default, so we're using VARCHAR with check constraint
-- If using ENUM, you would need to: ALTER TYPE order_status_enum ADD VALUE 'pending_payment' BEFORE 'pending';
-- and ALTER TYPE order_status_enum ADD VALUE 'payment_verified' BEFORE 'confirmed';
