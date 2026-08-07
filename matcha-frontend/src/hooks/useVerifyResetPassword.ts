import { useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import { verifyResetPassword } from "../services/auth"

export function useVerifyResetPassword() {
    const [searchParams] = useSearchParams()
    const [password, setPassword] = useState("")
    const navigate = useNavigate()
    const token = searchParams.get("token")
    const [error, setError] = useState<string | null>(null) 
    const [success, setSuccess] = useState<string | null>(null) 

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            if (!token) {
                setError("Token is missing.");
                return
            }

            const data = await verifyResetPassword(token, password)
            setSuccess(data.message)
            navigate("/login")

        } catch (err: unknown) {
            if (err instanceof Error) setError(err.message)
            else setError("An unexpected error occurred")
        }
    }

    return { password, setPassword, error, setError, success, setSuccess, handleSubmit }
}