import { useAuth } from "../context/AuthContext"
import Topbar from "../components/Topbar"

export default function Profile() {
  const { user, token, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
  }

  return (
    <div className="app-container">
        <Topbar></Topbar>
      <div className="brutal-card" style={{ background: "var(--accent)" }}>
        <h1>Mon Profil</h1>
        <hr border-width="3px" color="black" />
        
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <p><strong>ID :</strong> {user?.id}</p>
          <p><strong>Username :</strong> {user?.username}</p>
          <p><strong>Email :</strong> {user?.email}</p>
          <p><strong>Prénom :</strong> {user?.first_name || "Non renseigné"}</p>
          <p><strong>Nom :</strong> {user?.last_name || "Non renseigné"}</p>
        </div>

        <div style={{ marginTop: "20px", background: "white", padding: "10px", border: "2px solid black" }}>
          <p style={{ fontSize: "0.8rem", wordBreak: "break-all" }}>
            <strong>JWT Actuel :</strong> <br />
            {token?.substring(0, 50)}...
          </p>
        </div>
      </div>
    </div>
  )
}