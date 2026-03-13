import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
/* eslint-disable react-refresh/only-export-components */

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

interface AuthContextType {
  token: string | null
  setToken: (token: string | null) => void
  user: User | null
  setUser: (user: User | null) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  // 1. Initialisation avec le localStorage
  const [token, setTokenState] = useState<string | null>(localStorage.getItem("matcha_token"))
  const [user, setUser] = useState<User | null>(null)

  // 2. Fonction pour mettre à jour le token partout
  const setToken = (newToken: string | null) => {
    setTokenState(newToken)
    if (newToken) {
      localStorage.setItem("matcha_token", newToken)
    } else {
      localStorage.removeItem("matcha_token")
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
  }

  useEffect(() => {
    if (token && !user) {
      fetch("http://localhost:5000/me", {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        if (res.ok) return res.json()
        throw new Error("Token invalide")
      })
      .then(data => setUser(data.user))
      .catch(() => logout())
    }
  }, [token])

  return (
    <AuthContext.Provider value={{ 
      token, 
      setToken, 
      user, 
      setUser, 
      logout, 
      isAuthenticated: !!token 
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