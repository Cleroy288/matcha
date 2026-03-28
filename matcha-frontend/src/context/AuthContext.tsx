import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { API_ROUTES, fetchWithCredentials } from "../config/api"
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
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {

  const [user, setUser] = useState<User | null>(null)

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