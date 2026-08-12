import { useEffect, useRef, useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import { verifyResetPassword } from "../services/auth"

const REDIRECT_DELAY_MS = 3000

export function useVerifyResetPassword() {
    const [searchParams] = useSearchParams()
    const [password, setPassword] = useState("")
    const navigate = useNavigate()
    const token = searchParams.get("token")
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)
    const redirectTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

    // the timer must not outlive the page, otherwise it navigates from an unmounted component
    useEffect(() => () => {
        if (redirectTimer.current) clearTimeout(redirectTimer.current)
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        // 1 the token is single use: a second submit during the delay only yields a confusing error
        if (redirectTimer.current) return
        try {
            if (!token) {
                setError("Token is missing.");
                return
            }

            const data = await verifyResetPassword(token, password)
            setSuccess(data.message)
            redirectTimer.current = setTimeout(() => navigate("/login", { replace: true }), REDIRECT_DELAY_MS)

        } catch (err: unknown) {
            if (err instanceof Error) setError(err.message)
            else setError("An unexpected error occurred")
        }
    }

    return { password, setPassword, error, setError, success, setSuccess, handleSubmit }
}
