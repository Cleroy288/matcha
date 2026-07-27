import { createContext, useCallback, useContext, useState, useEffect, type ReactNode } from "react"
import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { useSocket } from "../hooks/useSocket"
import { fetchUnreadMessages } from "../services/chat"
import type { Message } from "../types/chat"
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
  unreadMessages: number
  refreshUnreadMessages: () => void
  incomingMessage: Message | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [unreadCount, setUnreadCount] = useState(0)
  const [unreadMessages, setUnreadMessages] = useState(0)
  const [incomingMessage, setIncomingMessage] = useState<Message | null>(null)

  // toute notification (like, visit, match, unlike, message) alimente le badge notifs
  const handleNotification = useCallback(() => {
    setUnreadCount(prev => prev + 1)
  }, [])

  // message temps réel : badge messages + relai vers la page chat si ouverte
  const handleMessage = useCallback((message: Message) => {
    setIncomingMessage(message)
    setUnreadMessages(prev => prev + 1)
  }, [])

  useSocket(handleNotification, user !== null, handleMessage)

  const refreshUnreadMessages = useCallback(() => {
    fetchUnreadMessages()
      .then(setUnreadMessages)
      .catch(() => {})
  }, [])

  // passé directement à onClick dans la Topbar : ne doit jamais rejeter, sinon
  // le navigateur logge un « Uncaught (in promise) » quand le backend est down
  const logout = async () => {
    try {
      await fetchWithCredentials(API_ROUTES.logout, { method: "POST" })
    } catch {
      // backend injoignable : on déconnecte quand même côté client
    }
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

  // compteurs initiaux au login (notifs + messages non lus)
  useEffect(() => {
    if (!user) return

    fetchWithCredentials(API_ROUTES.notificationsUnread)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            if (data) setUnreadCount(data.count)
        })
        .catch(() => {})

    refreshUnreadMessages()
  }, [user, refreshUnreadMessages])

  return (
    <AuthContext.Provider value={{
      user,
      setUser,
      logout,
      isAuthenticated: user !== null,
      unreadCount,
      setUnreadCount,
      unreadMessages,
      refreshUnreadMessages,
      incomingMessage
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
