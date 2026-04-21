import { useState } from "react"
import { register } from "../services/auth"

export function useRegister() {
  const [first_name, setFirstName] = useState("")
  const [last_name, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const data = await register({ first_name, last_name, email, username, password })
      setSuccess(data.message)
    } catch (err: unknown) {
        if (err instanceof Error) {
            setError(err.message)
        } else {
            setError("Une erreur inattendue est survenue")
        }
    }
  }

  return { first_name, setFirstName, last_name, setLastName, email, setEmail,
        username, setUsername, password, setPassword,
        error, setError, success, setSuccess, handleSubmit }
}