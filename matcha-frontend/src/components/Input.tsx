import "./Input.css"

type InputProps = React.InputHTMLAttributes<HTMLInputElement>

export default function Input({ children, ...props }: InputProps) {
  return (
    <input {...props} className="Input">
      {children}
    </input>
  )
}