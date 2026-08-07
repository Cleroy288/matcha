import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import Button from "./Button"
import './Topbar.css'
import ThemeSelector from "./ThemeSelector"

export default function Topbar() {
  const { user, isAuthenticated, logout, unreadCount, unreadMessages } = useAuth()
  return (
    <nav className="topbar">
      <div className="topbar-logo">MATCHA</div>
      <ThemeSelector></ThemeSelector>
      <div className="topbar-links">
        {isAuthenticated ? (
          <>
            <span className="topbar-welcome">Welcome, {user?.username}</span>
            <Link to="/home" className="nav-item">Home</Link>
            <Link to="/search" className="nav-item">Search</Link>
            <Link to="/chat" className={`notif-btn ${unreadMessages > 0 ? "notif-btn--active" : ""}`}>
                Chat
                {unreadMessages > 0 && (
                    <span className="notif-badge">
                    {unreadMessages > 99 ? "99+" : unreadMessages}
                    </span>
                )}
            </Link>
            <Link to="/profile/edit" className="nav-item">Profile</Link>
            <Link to="/notification" className={`notif-btn ${unreadCount > 0 ? "notif-btn--active" : ""}`}>
                Notifs
                {unreadCount > 0 && (
                    <span className="notif-badge">
                    {unreadCount > 99 ? "99+" : unreadCount}
                    </span>
                )}
            </Link>
            <Button onClick={logout} className="btn-logout">Logout</Button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-item">Login</Link>
            <Link to="/register" className="nav-item">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}
