import Topbar from "../components/Topbar"
import Input from "../components/Input"
import { useState } from "react"
import Button from "../components/Button"

export default function Register(){
      const [username, setUsername] = useState("")
      const [password, setPassword] = useState("")
      const [first_name, setFirstName] = useState("")
      const [last_name, setLastName] = useState("")
      const [email, setEmail] = useState("")
    
      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
          const res = await fetch("http://localhost:5000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, username, password, first_name, last_name })
          })
          const data = await res.json()
          if (res.ok) {
            console.log("register success")
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
            <h1>Register</h1>
            <Topbar></Topbar>
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
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <Button type="submit"> Register </Button>
                  </form>
        </div>
    )
}