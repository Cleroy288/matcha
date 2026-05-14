import { useEffect, useRef } from "react"
import { io, Socket } from "socket.io-client"
import { API_BASE_URL } from "../config/api"

export function useSocket(onNotification: (notif: { type: string; data: unknown }) => void, enabled = true) {
    const socketRef = useRef<Socket | null>(null)

    useEffect(() => {
        if (!enabled) return

        socketRef.current = io(API_BASE_URL, {
            withCredentials: true,
        })

        socketRef.current.on("new_notification", (notif) => {
            console.log("Notif reçue :", notif)
            onNotification(notif)
        })

        return () => {
            socketRef.current?.disconnect()
        }
    }, [enabled, onNotification])
}
