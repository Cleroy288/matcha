import type { SelectHTMLAttributes } from "react"
import "./Select.css"

type SelectProps = SelectHTMLAttributes<HTMLSelectElement>

export default function Select({ children, ...props }: SelectProps) {
  return (
    <select {...props} className="Select">
      {children}
    </select>
  )
}
