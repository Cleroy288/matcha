import { useState, useEffect } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import { verifyEmail } from "../services/auth"

export function useVerifyEmail() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const token = searchParams.get("token")
  const [status, setStatus] = useState<"loading" | "success" | "error">(token ? "loading" : "error")
  const [message, setMessage] = useState(token ? "Vérification en cours..." : "Token manquant.")

  useEffect(() => {
    if (!token) return

    verifyEmail(token)
      .then(data => {
        setStatus("success")
        setMessage(data.message)
        setTimeout(() => navigate("/login"), 3000)
      })
      .catch((err: unknown) => {
        setStatus("error")
        // le backend explique pourquoi (lien expiré, déjà utilisé…) : ne pas
        // écraser son message par un diagnostic réseau faux
        setMessage(err instanceof Error ? err.message : "Impossible de contacter le serveur.")
      })
  }, [token, navigate])

  return { status, message }
}