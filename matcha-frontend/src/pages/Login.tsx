import { useState } from "react"
import { useAuth } from "../context/AuthContext.tsx"
import Button from "../components/Button.tsx"
import Input from "../components/Input.tsx"
import Topbar from "../components/Topbar.tsx"

export default function Login() {
  const { setToken, setUser } = useAuth()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      })
      const data = await res.json()
      if (res.ok) {
        console.log("login success")
        setToken(data.token)
        setUser(data.user)
      } else {
        console.log("error")
        alert(data.error)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="app-container">
        <Topbar></Topbar>
      <h1>Connexion</h1>
      <form onSubmit={handleSubmit} className="brutal-card">
        <Input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit"> Login </Button>
      </form>
    </div>
  )
}