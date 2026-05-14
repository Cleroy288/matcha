import { createContext, useCallback, useContext, useState, useEffect, type ReactNode } from "react"
import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { useSocket } from "../hooks/useSocket"
/* eslint-disable react-refresh/only-export-components */

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

interface AuthContextType {
  user: User | null
  setUser: (user: User | null) => void
  logout: () => void
  isAuthenticated: boolean
  unreadCount: number
  setUnreadCount: (count: number) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [unreadCount, setUnreadCount] = useState(0)

  const handleNotification = useCallback((notif: { type: string; data: unknown }) => {
    if (notif.type === "like" || notif.type === "match" || notif.type === "visit") {
        setUnreadCount(prev => prev + 1)  // ← incrémente le badge
    }
  }, [])

  useSocket(handleNotification, user !== null)
  const logout = async () => {
    await fetchWithCredentials(API_ROUTES.logout, { method: "POST" })
    setUser(null)
  }

  useEffect(() => {
    fetchWithCredentials(API_ROUTES.me)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            if (data) setUser(data.user)
        })
        .catch(() => {})
  }, [])

  return (
    <AuthContext.Provider value={{ 
      user, 
      setUser, 
      logout,
      isAuthenticated: user !== null,
      unreadCount,
      setUnreadCount
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used within an AuthProvider")
  return context
}
