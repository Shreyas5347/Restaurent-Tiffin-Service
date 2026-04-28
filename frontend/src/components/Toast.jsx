import { useEffect, useState } from 'react';
import './Toast.css';

export default function Toast({ message, emoji = '✅', visible, onHide }) {
  const [animating, setAnimating] = useState(false);

  useEffect(() => {
    if (visible) {
      setAnimating(true);
      const timer = setTimeout(() => {
        setAnimating(false);
        setTimeout(onHide, 350); // wait for exit animation
      }, 2200);
      return () => clearTimeout(timer);
    }
  }, [visible, onHide]);

  if (!visible && !animating) return null;

  return (
    <div className={`toast ${animating ? 'toast--visible' : 'toast--hiding'}`} role="status" aria-live="polite">
      <span className="toast__emoji">{emoji}</span>
      <span className="toast__message">{message}</span>
    </div>
  );
}
