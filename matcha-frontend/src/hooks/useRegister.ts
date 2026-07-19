import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { login, register } from "../services/auth"

export function useRegister() {
  const { setUser } = useAuth()
  const navigate = useNavigate()
  const [first_name, setFirstName] = useState("")
  const [last_name, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    setError(null)
    try {
      const data = await register({
        first_name,
        last_name,
        email,
        username,
        password,
        confirm_password: confirmPassword,
      })
      setSuccess(data.message)
      if (!data.email_verification_required) {
        const session = await login({ username, password })
        setUser(session.user)
        navigate("/profile/edit", { replace: true })
      }
    } catch (err: unknown) {
        if (err instanceof Error) {
            setError(err.message)
        } else {
            setError("Une erreur inattendue est survenue")
        }
    }
  }

  return { first_name, setFirstName, last_name, setLastName, email, setEmail,
        username, setUsername, password, setPassword, confirmPassword, setConfirmPassword,
        error, setError, success, setSuccess, handleSubmit }
}
