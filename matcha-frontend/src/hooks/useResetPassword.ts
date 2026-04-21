import { useState } from "react"
import { resetPassword } from "../services/auth"

export function useResetPassword() {
    const [email, setEmail] = useState("")
    const [error, setError] = useState<string | null>(null) 
    const [success, setSuccess] = useState<string | null>(null) 

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const data =  await resetPassword(email)
            setSuccess(data.message)
        } catch (err: unknown) {
            if (err instanceof Error) setError(err.message)
            else setError("Une erreur inattendue est survenue")
        }
    }

  return { email, setEmail, error, setError, success, setSuccess, handleSubmit }
}