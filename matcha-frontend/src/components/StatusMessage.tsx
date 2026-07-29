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

  const onCloseRef = useRef(onClose)
  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])

  useEffect(() => {
    const timer = setTimeout(() => {
      onCloseRef.current()
    }, duration)

    return () => clearTimeout(timer)
  }, [message, duration])

  return (
    <div className={`status-message status-${type}`}>
      <div className="status-icon">{icons[type]}</div>
      <span>{message}</span>
      <button className="status-close" onClick={onClose}>✕</button>
    </div>
  )
}
