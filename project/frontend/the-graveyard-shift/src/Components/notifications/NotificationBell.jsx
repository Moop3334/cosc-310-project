import { useState, useEffect, useRef } from 'react';
import { notificationAPI } from '../../services/api';
import './styles/NotificationBell.css';

const POLL_INTERVAL = 30000; // 30 seconds

export default function NotificationBell() {
  const [notifications, setNotifications] = useState([]);
  const [open, setOpen] = useState(false);
  const panelRef = useRef(null);

  const userId = localStorage.getItem('userId');

  const fetchNotifications = async () => {
    if (!userId) return;
    try {
      const data = await notificationAPI.getNotifications(userId);
      setNotifications(data);
    } catch {
      // silent — bell just shows nothing
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [userId]);

  // Close panel when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [open]);

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  const handleOpen = async () => {
    const wasOpen = open;
    setOpen(!wasOpen);

    // Mark all as read when opening
    if (!wasOpen && unreadCount > 0 && userId) {
      try {
        await notificationAPI.markAsRead(userId);
        setNotifications((prev) =>
          prev.map((n) => ({ ...n, is_read: true }))
        );
      } catch {
        // silent
      }
    }
  };

  return (
    <div className="notification-bell-wrapper" ref={panelRef}>
      <button className="notification-bell-btn" onClick={handleOpen} aria-label="Notifications">
        <span className="bell-icon">🔔</span>
        {unreadCount > 0 && (
          <span className="notification-badge">{unreadCount}</span>
        )}
      </button>

      {open && (
        <div className="notification-panel">
          <div className="notification-panel-header">
            <h3>Notifications</h3>
          </div>
          <div className="notification-panel-body">
            {notifications.length === 0 ? (
              <p className="no-notifications">No notifications yet.</p>
            ) : (
              <ul className="notification-list">
                {[...notifications].reverse().map((n) => (
                  <li key={n.id} className={`notification-item ${n.is_read ? '' : 'unread'}`}>
                    <p className="notification-message">{n.message}</p>
                    <span className="notification-time">
                      {new Date(n.created_at).toLocaleString()}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}