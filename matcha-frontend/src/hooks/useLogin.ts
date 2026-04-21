import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import { login } from "../services/auth"

export function useLogin() {
  const { setUser } = useAuth()
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
    } catch (err: unknown) {
        if (err instanceof Error) {
            setError(err.message)
        } else {
            setError("Une erreur inattendue est survenue")
        }
    }
  }

  return { username, setUsername, password, setPassword,
           error, setError, success, setSuccess, handleSubmit }
}