import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { login } from "../services/auth"
import { getPostLoginRoute } from "../utils/authRoute"

export function useLogin() {
  const { setUser } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const data = await login({ username, password })
      setUser(data.user)
      setSuccess(data.message)
      const requestedPath = (location.state as { from?: string } | null)?.from
      navigate(getPostLoginRoute(data.user, requestedPath), { replace: true })
    } catch (err: unknown) {
        if (err instanceof Error) {
            setError(err.message)
        } else {
            setError("An unexpected error occurred")
        }
    }
  }

  return { username, setUsername, password, setPassword,
           error, setError, success, setSuccess, handleSubmit }
}
