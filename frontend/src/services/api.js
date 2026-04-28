const BASE_URL = 'http://localhost:5000';

/**
 * Fetch all menu items from the Flask backend.
 * Endpoint: GET /menu/items
 */
export async function fetchMenuItems() {
  const response = await fetch(`${BASE_URL}/menu/items`);
  if (!response.ok) {
    throw new Error(`Failed to fetch menu items (${response.status})`);
  }
  return response.json();
}
