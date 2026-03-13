import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import Button from "./Button"
import './Topbar.css'

export default function Topbar() {
  const { user, isAuthenticated, logout } = useAuth()

  return (
    <nav className="topbar">
      <div className="topbar-logo">MATCHA</div>
      <div className="topbar-links">
        {isAuthenticated ? (
          <>
            <span>Welcome, {user?.username}</span>
            <Link to="/profile" className="nav-item">Profil</Link>
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