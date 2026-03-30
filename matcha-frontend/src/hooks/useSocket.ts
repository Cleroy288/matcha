import { useEffect, useRef } from "react"
import { io, Socket } from "socket.io-client"
import { API_BASE_URL } from "../config/api"

export function useSocket(onNotification: (notif: { type: string; data: unknown }) => void) {
    const socketRef = useRef<Socket | null>(null)

    useEffect(() => {
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
    }, [])
}