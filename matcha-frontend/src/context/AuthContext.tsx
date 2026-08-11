import { createContext, useCallback, useContext, useState, useEffect, type ReactNode } from "react"
import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { useSocket } from "../hooks/useSocket"
import { fetchUnreadMessages } from "../services/chat"
import type { Message } from "../types/chat"
import type { User } from "../types/auth"
/* eslint-disable react-refresh/only-export-components */

interface AuthContextType {
  user: User | null
  setUser: (user: User | null) => void
  logout: () => Promise<void>
  isAuthenticated: boolean
  authLoading: boolean
  unreadCount: number
  setUnreadCount: (count: number) => void
  unreadMessages: number
  refreshUnreadMessages: () => void
  incomingMessage: Message | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [unreadCount, setUnreadCount] = useState(0)
  const [unreadMessages, setUnreadMessages] = useState(0)
  const [incomingMessage, setIncomingMessage] = useState<Message | null>(null)

  // every notification (like, visit, match, unlike, message) feeds the notification badge
  const handleNotification = useCallback(() => {
    setUnreadCount(prev => prev + 1)
  }, [])

  // real-time message: message badge + relay to the chat page when it is open
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

  // passed straight to onClick in the Topbar: it must never reject, otherwise
  // the browser logs an "Uncaught (in promise)" when the backend is down
  const logout = async () => {
    await fetchWithCredentials(API_ROUTES.logout, { method: "POST" }).catch(() => {})
    setUser(null)
  }

  useEffect(() => {
    fetchWithCredentials(API_ROUTES.me)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            if (data) setUser(data.user)
        })
        .catch(() => {})
        .finally(() => setAuthLoading(false))
  }, [])

  // initial counters at login (notifications + unread messages)
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
      authLoading,
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
