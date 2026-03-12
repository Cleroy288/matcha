import { useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import Topbar from "../components/Topbar"
import Input from "../components/Input"
import Button from "../components/Button"

export default function VerifyResetPassword() {
  const [searchParams] = useSearchParams()
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const token = searchParams.get("token")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`http://localhost:5000/verify-reset-password?token=${token}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
      })
      if (res.ok) {
        alert("Mot de passe modifié !")
        navigate("/login")
      } else {
        const data = await res.json()
        alert(data.error)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="app-container">
      <Topbar />
      <h1>Nouveau mot de passe</h1>
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