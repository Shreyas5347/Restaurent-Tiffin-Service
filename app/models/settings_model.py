import json
import os
from datetime import datetime, time, timezone, timedelta
from app.database.db import get_db_connection

try:
    from zoneinfo import ZoneInfo
    IST_TZ = ZoneInfo("Asia/Kolkata")
except Exception:
    IST_TZ = timezone(timedelta(hours=5, minutes=30))

# Operating time slots (24-hour format)
# Morning: 10:00 AM - 2:00 PM (10:00 - 14:00)
# Evening: 6:00 PM - 10:00 PM (18:00 - 22:00)
OPERATING_SLOTS = [
    {
        "name": "Morning Slot",
        "start": "10:00",
        "end": "14:00",
        "label": "10:00 AM – 2:00 PM"
    },
    {
        "name": "Evening Slot",
        "start": "18:00",
        "end": "22:00",
        "label": "6:00 PM – 10:00 PM"
    }
]

FALLBACK_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "shop_settings.json")


def _init_settings_table(conn):
    """Ensure system_settings table exists."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key VARCHAR(50) PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Seed default mode if not present
        cursor.execute("""
            INSERT INTO system_settings (key, value)
            VALUES ('shop_mode', 'auto')
            ON CONFLICT (key) DO NOTHING;
        """)
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        # Non-fatal if table creation fails


def _get_mode_from_file():
    try:
        if os.path.exists(FALLBACK_SETTINGS_FILE):
            with open(FALLBACK_SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("mode", "auto")
    except Exception:
        pass
    return "auto"


def _set_mode_to_file(mode):
    try:
        with open(FALLBACK_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"mode": mode, "updated_at": datetime.now().isoformat()}, f)
    except Exception:
        pass


def get_current_ist_time():
    """Get current datetime in IST."""
    try:
        return datetime.now(IST_TZ)
    except Exception:
        return datetime.now()


def is_within_operating_hours(now_dt=None):
    """Check if current time is within morning 10-2pm or evening 6-10pm."""
    if now_dt is None:
        now_dt = get_current_ist_time()
    
    current_time = now_dt.time()
    
    # Morning: 10:00 to 14:00
    morning_start = time(10, 0, 0)
    morning_end = time(14, 0, 0)
    
    # Evening: 18:00 to 22:00
    evening_start = time(18, 0, 0)
    evening_end = time(22, 0, 0)
    
    if morning_start <= current_time < morning_end:
        return True, "Morning Slot (10:00 AM – 2:00 PM)"
    elif evening_start <= current_time < evening_end:
        return True, "Evening Slot (6:00 PM – 10:00 PM)"
    else:
        return False, None


def get_shop_mode():
    """Fetch current mode: 'auto', 'open' (force open), or 'closed' (force closed)."""
    try:
        conn = get_db_connection()
        _init_settings_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM system_settings WHERE key = 'shop_mode';")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and row[0]:
            return row[0].strip().lower()
    except Exception:
        pass
    return _get_mode_from_file()


def set_shop_mode(mode):
    """Set mode: 'auto' | 'open' | 'closed'."""
    mode = mode.strip().lower()
    if mode not in {"auto", "open", "closed"}:
        raise ValueError("Mode must be 'auto', 'open', or 'closed'")
    
    _set_mode_to_file(mode)
    
    try:
        conn = get_db_connection()
        _init_settings_table(conn)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_settings (key, value, updated_at)
            VALUES ('shop_mode', %s, CURRENT_TIMESTAMP)
            ON CONFLICT (key) DO UPDATE
            SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP;
        """, (mode,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass
    
    return mode


def get_shop_status():
    """
    Get full shop status object with timings, open state, and mode.
    """
    mode = get_shop_mode()
    now_dt = get_current_ist_time()
    in_hours, current_slot = is_within_operating_hours(now_dt)
    
    if mode == "open":
        is_open = True
        status_message = "Open for orders (Admin Force Open)"
    elif mode == "closed":
        is_open = False
        status_message = "Currently closed for orders (Admin Force Closed)"
    else:
        # Auto schedule
        is_open = in_hours
        if is_open:
            status_message = f"Open for orders - {current_slot}"
        else:
            status_message = "Currently closed for orders. Ordering hours: 10:00 AM - 2:00 PM & 6:00 PM - 10:00 PM"
            
    return {
        "is_open": is_open,
        "mode": mode,
        "current_slot": current_slot,
        "status_message": status_message,
        "current_time": now_dt.strftime("%I:%M %p"),
        "slots": OPERATING_SLOTS,
        "timings_summary": "Morning: 10:00 AM – 2:00 PM | Evening: 6:00 PM – 10:00 PM"
    }


def is_shop_open():
    """Convenience boolean check used in order placement."""
    status = get_shop_status()
    return status["is_open"], status["status_message"]
