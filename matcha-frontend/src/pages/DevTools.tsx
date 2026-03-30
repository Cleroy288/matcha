import { useState } from "react"
import Topbar from "../components/Topbar"
import { fetchWithCredentials, API_ROUTES } from "../config/api"

export default function DevTools() {
  const [targetId, setTargetId] = useState("")
  const [result, setResult] = useState<string | null>(null)

  const call = async (method: string, url: string, label: string) => {
    try {
      const res = await fetchWithCredentials(url, { method })
      const data = await res.json()
      setResult(`[${label}] ${JSON.stringify(data, null, 2)}`)
    } catch (e) {
      setResult(`[${label}] ERREUR: ${e}`)
    }
  }

  return (
    <div className="app-container">
      <Topbar />
      <h1>Dev Tools</h1>

      <div className="brutal-card" style={{ background: "var(--matcha-light)", minWidth: "400px" }}>
        <h2>Target user ID</h2>
        <input
          type="number"
          placeholder="ID de l'user cible"
          value={targetId}
          onChange={e => setTargetId(e.target.value)}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          <button onClick={() => call("POST", `${API_ROUTES.like}/${targetId}`, "LIKE")}>
            Like user {targetId || "?"}
          </button>
          <button onClick={() => call("DELETE", `${API_ROUTES.like}/${targetId}`, "UNLIKE")}>
            Unlike user {targetId || "?"}
          </button>
          <button onClick={() => call("POST", `${API_ROUTES.visit}/${targetId}`, "VISIT")}>
            Visiter profil {targetId || "?"}
          </button>
          <button onClick={() => call("POST", `${API_ROUTES.block}/${targetId}`, "BLOCK")}>
            Bloquer user {targetId || "?"}
          </button>
          <button onClick={() => call("GET", API_ROUTES.notifications, "NOTIFS")}>
            Voir mes notifs
          </button>
          <button onClick={() => call("GET", API_ROUTES.notificationsUnread, "UNREAD COUNT")}>
            Compter notifs non lues
          </button>
          <button onClick={() => call("GET", `${API_ROUTES.me}`, "ME")}>
            Qui suis-je ?
          </button>
        </div>
      </div>

      {result && (
        <div style={{
          marginTop: "1.5rem",
          background: "#000",
          color: "#BEF264",
          padding: "1rem",
          border: "3px solid #000",
          fontFamily: "monospace",
          whiteSpace: "pre",
          maxWidth: "500px",
          width: "100%",
          boxShadow: "var(--brutal-shadow)"
        }}>
          {result}
        </div>
      )}
    </div>
  )
}