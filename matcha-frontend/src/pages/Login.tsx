import { useState } from "react"
import { useAuth } from "../context/AuthContext.tsx"
import Button from "../components/Button.tsx"
import Input from "../components/Input.tsx"
import Topbar from "../components/Topbar.tsx"
import { Link } from "react-router-dom"
import { API_ROUTES, fetchWithCredentials } from "../config/api.ts"
import StatusMessage from "../components/StatusMessage.tsx"

export default function Login() {
  const { setUser } = useAuth()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null) 
  const [success, setSucces] = useState<string | null>(null) 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetchWithCredentials(`${API_ROUTES.login}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      })
      const data = await res.json()
      if (res.ok) {
        console.log("login success")
        setUser(data.user)
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
        <Topbar></Topbar>
      <h1>Se connecter</h1>
      {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
      {success && <StatusMessage type="success" message={success} onClose={() => setSucces(null)}/>} 
      <form onSubmit={handleSubmit} className="brutal-card">
        <Input
          type="text"
          placeholder="Username"
          value={username}
          autoComplete="username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          autoComplete="current-password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit"> Login </Button>
      </form>
      <Link to="/reset-password" className="link">Reset Password</Link>
    </div>
  )
}