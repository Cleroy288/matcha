import Topbar from "../components/Topbar";
import Input from "../components/Input";
import Button from "../components/Button";
import { useState } from "react"

export default function ResetPassword() {

    const [email, setemail] = useState("")
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
        const res = await fetch("http://localhost:5000/reset-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email})
        })
        const data = await res.json()
        if (res.ok) {
            console.log("RESET PASSWORD success")
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
            <h1>Reset Password</h1>
            <form onSubmit={handleSubmit} className="brutal-card">
                    <Input
                      type="email"
                      placeholder="email"
                      value={email}
                      autoComplete="email"
                      onChange={(e) => setemail(e.target.value)}
                    />

                    <Button type="submit"> send mail </Button>
                  </form>
        </div>
    )
}