import { useEffect, useRef } from "react"
import { io, Socket } from "socket.io-client"
import { API_BASE_URL } from "../config/api"
import type { Message } from "../types/chat"

export interface SocketNotification {
  type: string
  data: unknown
}

/* Connexion WebSocket authentifiée (cookie) : notifications + messages temps réel */
export function useSocket(
  onNotification: (notif: SocketNotification) => void,
  enabled = true,
  onMessage?: (message: Message) => void
) {
  const socketRef = useRef<Socket | null>(null)

  useEffect(() => {
    if (!enabled) return

    socketRef.current = io(API_BASE_URL, {
      withCredentials: true,
    })

    socketRef.current.on("new_notification", (notif) => {
      onNotification(notif)
    })

    socketRef.current.on("new_message", (message: Message) => {
      onMessage?.(message)
    })

    return () => {
      socketRef.current?.disconnect()
    }
  }, [enabled, onNotification, onMessage])
}
