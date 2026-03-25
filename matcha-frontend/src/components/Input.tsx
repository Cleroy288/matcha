import type { InputHTMLAttributes } from "react"
import "./Input.css"

type InputProps = InputHTMLAttributes<HTMLInputElement>

export default function Input({ children, ...props }: InputProps) {
  return (
    <input {...props} className="Input">
      {children}
    </input>
  )
}
