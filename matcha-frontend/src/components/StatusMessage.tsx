import { useEffect } from "react"
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

  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, duration)

    return () => clearTimeout(timer)  // ← cleanup si le composant disparaît avant
  }, [message])                       // ← se relance si un nouveau message arrive

  return (
    <div className={`status-message status-${type}`}>
      <div className="status-icon">{icons[type]}</div>
      <span>{message}</span>
      <button className="status-close" onClick={onClose}>✕</button>
    </div>
  )
}
