import { useEffect, useRef } from "react"
import "./StatusMessage.css"

type StatusType = "error" | "success" | "info"

const icons = { error: "✕", success: "✓", info: "i" }

type Props = {
  type: StatusType
  message: string
  onClose: () => void
  duration?: number
}

export default function StatusMessage({ type, message, onClose, duration = 5000 }: Props) {
  // parents often pass an inline onClose: the latest version is kept in a ref
  // so the timer is not re-armed on every render
  const onCloseRef = useRef(onClose)
  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])

  useEffect(() => {
    const timer = setTimeout(() => {
      onCloseRef.current()
    }, duration)

    return () => clearTimeout(timer)  // ← cleanup if the component unmounts first
  }, [message, duration])             // ← restarts when a new message arrives

  return (
    <div className={`status-message status-${type}`}>
      <div className="status-icon">{icons[type]}</div>
      <span>{message}</span>
      <button className="status-close" onClick={onClose}>✕</button>
    </div>
  )
}
