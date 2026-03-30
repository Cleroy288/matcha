import Topbar from "../components/Topbar"
import Input from "../components/Input"
import { useState } from "react"
import Button from "../components/Button"
import { API_ROUTES } from "../config/api"
import StatusMessage from "../components/StatusMessage"

export default function Register(){
      const [username, setUsername] = useState("")
      const [password, setPassword] = useState("")
      const [first_name, setFirstName] = useState("")
      const [last_name, setLastName] = useState("")
      const [email, setEmail] = useState("")
      const [error, setError] = useState<string | null>(null) 
      const [success, setSucces] = useState<string | null>(null) 

      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
          const res = await fetch(`${API_ROUTES.register}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, username, password, first_name, last_name })
          })
          const data = await res.json()
          if (res.ok) {
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
            <h1>Register</h1>
            <Topbar></Topbar>
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
            {success && <StatusMessage type="success" message={success} onClose={() => setSucces(null)}/>} 
            <form onSubmit={handleSubmit} className="brutal-card">
                <Input
                    type="text"
                    placeholder="First name"
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                />
                <Input
                    type="text"
                    placeholder="Last name"
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                />
                <Input
                    type="email"
                    placeholder="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <Input
                    type="text"
                    placeholder="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <Input
                    type="password"
                    placeholder="Password"
                    value={password}
                    autoComplete="new-password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button type="submit"> Register </Button>
                </form>
        </div>
    )
}