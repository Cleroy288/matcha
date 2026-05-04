import { Link } from "react-router-dom"
import Topbar from "../components/Topbar.tsx"
import { useVerifyEmail } from "../hooks/useVerifyEmail.ts"

export default function VerifyEmail() {
    const {status, message} = useVerifyEmail()

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