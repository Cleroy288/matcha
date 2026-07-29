import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"
import Topbar from "../components/Topbar"
import { fetchNotifications, markNotificationsRead } from "../services/notification"
import type { Notification } from "../types/notification"

const TYPE_LABELS: Record<string, string> = {
  like:    "liked your profile",
  visit:   "viewed your profile",
  match:   "it's a match!",
  unlike:  "removed their like",
  message: "sent you a message",
}

const TYPE_COLORS: Record<string, string> = {
  like:    "var(--primary)",
  match:   "var(--accent)",
  visit:   "var(--matcha-light)",
  unlike:  "#e0e0e0",
  message: "var(--primary)",
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString("en-GB", {
    day: "numeric", month: "short", hour: "2-digit", minute: "2-digit"
  })
}

export default function Notifications() {
  const { isAuthenticated, setUnreadCount } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!isAuthenticated) return

    fetchNotifications()
      .then(data => {
        setNotifications(data.notifications)
        return markNotificationsRead()
      })
      .then(() => setUnreadCount(0))
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "Server error"))
      .finally(() => setLoading(false))
  }, [isAuthenticated, setUnreadCount])

  if (!isAuthenticated) {
    return (
      <div className="app-container">
        <Topbar />
        <h1>Please log in</h1>
      </div>
    )
  }

  return (
    <div className="app-container page-scroll">
      <Topbar />
      <h1>Notifications</h1>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && notifications.length === 0 && (
        <div className="brutal-card" style={{ background: "var(--matcha-light)", textAlign: "center" }}>
          <p>No notifications yet.</p>
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "1rem", width: "100%", maxWidth: "600px" }}>
        {notifications.map(notif => (
          <div
            key={notif.id}
            style={{
              background: TYPE_COLORS[notif.type] ?? "white",
              border: "3px solid var(--black)",
              boxShadow: notif.is_read ? "none" : "var(--brutal-shadow)",
              padding: "1rem 1.25rem",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              opacity: notif.is_read ? 0.7 : 1,
            }}
          >
            <div>
              <strong>{notif.username ?? "Someone"}</strong>
              {" "}{TYPE_LABELS[notif.type] ?? notif.type}
            </div>
            <span style={{ fontSize: "0.8rem", fontWeight: 600, whiteSpace: "nowrap" }}>
              {formatDate(notif.created_at)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
