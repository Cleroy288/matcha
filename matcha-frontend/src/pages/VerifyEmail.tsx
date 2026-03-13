import { useEffect, useState } from "react"
import { useSearchParams, useNavigate, Link } from "react-router-dom"
import Topbar from "../components/Topbar.tsx"

export default function VerifyEmail() {
  const [searchParams] = useSearchParams()
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading")
  const [message, setMessage] = useState("Vérification en cours...")
  const navigate = useNavigate()

  useEffect(() => {
    const verify = async () => {
    const token = searchParams.get("token")

    if (!token) {
      setStatus("error")
      setMessage("Token de vérification manquant.")
      return
    }

    fetch(`http://localhost:5000/verify-email?token=${token}`)
      .then(async (res) => {
        const data = await res.json()
        if (res.ok) {
          setStatus("success")
          setMessage(data.message)
          // On redirige vers le login après 3 secondes pour qu'il ait le temps de lire
          setTimeout(() => navigate("/login"), 3000)
        } else {
          setStatus("error")
          setMessage(data.error || "Une erreur est survenue.")
        }
      })
      .catch(() => {
        setStatus("error")
        setMessage("Impossible de contacter le serveur.")
      })
      }

    verify()
  }, [searchParams, navigate])

  return (
    <div className="app-container">
      <Topbar />
      <div style={{ marginTop: "100px" }}>
        <div className="brutal-card" style={{ 
          textAlign: "center", 
          background: status === "success" ? "#9eff9e" : status === "error" ? "#ff9e9e" : "white" 
        }}>
          <h1>Vérification</h1>
          <p>{message}</p>
          
          {status === "success" && (
            <p style={{ fontSize: "0.8rem" }}>Redirection vers la page de connexion...</p>
          )}
          
          {status === "error" && (
            <Link to="/login">
               <button className="brutal-button" style={{marginTop: "20px"}}>Retour au Login</button>
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}