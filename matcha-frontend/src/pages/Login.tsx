import { useState } from "react"
import { useAuth } from "../context/AuthContext.tsx"
import Button from "../components/Button.tsx"
import Input from "../components/Input.tsx"
import Topbar from "../components/Topbar.tsx"
import { Link } from "react-router-dom"
import { API_ROUTES, fetchWithCredentials } from "../config/api.ts"
import StatusMessage from "../components/StatusMessage.tsx"

import TwoCoeur from "../assets/doublecoeur.svg?react"
import Couple from "../assets/cup2.svg?react"
import Cup4 from "../assets/cup4.svg?react"
import Cupi from "../assets/coeurcupidon.svg?react"
// import Symbole2 from "../assets/love.svg?react"
import CupTchin from "../assets/cupTchin.svg?react"
import OiseauVol from "../assets/oiseauCoeur.svg?react"


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
        <TwoCoeur className="sil sil-accent sil-left-in sil-xs sil-middle-up sil-flip-x sil-float" />
        <Cup4 className="sil sil-primary sil-left-in sil-xs sil-middle-cup4 sil-float-alt" />
        
        
        <OiseauVol className="sil sil-accent sil-left-mid-center sil-xs sil-middle-down sil-sway-hg sil-shadow-primary" />
        
        <CupTchin className="sil sil-color-topbar-border sil-left-mid sil-sm sil-bottom sil-flip-x" />
        {/* <Symbole2 className="sil sil-primary sil-left sil-xs sil-bottom " /> */}
        <Cupi className="sil sil-color-topbar-border sil-right-mid sil-xxs sil-xs sil-middle-cupi sil-sway-shadow sil-shadow-accent" />
        <Couple className="sil sil-accent sil-right-in sil-md " />
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