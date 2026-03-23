import { useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import Topbar from "../components/Topbar"
import Input from "../components/Input"
import Button from "../components/Button"
import { API_ROUTES } from "../config/api"
import StatusMessage from "../components/StatusMessage"

export default function VerifyResetPassword() {
  const [searchParams] = useSearchParams()
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const token = searchParams.get("token")
  const [error, setError] = useState<string | null>(null) 
  const [success, setSucces] = useState<string | null>(null) 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_ROUTES.verifyResetPassword}?token=${token}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
      })
      const data = await res.json()
      if (res.ok) {
          navigate("/login")
        setSucces(data.message)
      } else {
        setError(data.error)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="app-container">
      <Topbar />
      <h1>Nouveau mot de passe</h1>
      {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
      {success && <StatusMessage type="success" message={success} onClose={() => setSucces(null)}/>} 
      <form onSubmit={handleSubmit} className="brutal-card">
        <Input 
          type="password" 
          placeholder="New Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <Button type="submit">Changer le mot de passe</Button>
      </form>
    </div>
  )
}