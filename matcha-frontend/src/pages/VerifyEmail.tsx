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
          <h1>Verification</h1>
          <p>{message}</p>
          
          {status === "success" && (
            <p style={{ fontSize: "0.8rem" }}>Redirecting to the login page...</p>
          )}
          
          {status === "error" && (
            <Link to="/login">
               <button className="brutal-button" style={{marginTop: "20px"}}>Back to login</button>
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}