import Topbar from "../components/Topbar";
import Input from "../components/Input";
import Button from "../components/Button";
import { useState } from "react"
import { API_ROUTES } from "../config/api";
import StatusMessage from "../components/StatusMessage";

export default function ResetPassword() {

    const [email, setemail] = useState("")
    const [error, setError] = useState<string | null>(null) 
    const [success, setSucces] = useState<string | null>(null) 

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
        const res = await fetch(`${API_ROUTES.resetPassword}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email})
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
            <Topbar></Topbar>
            <h1>Reset Password</h1>
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
            {success && <StatusMessage type="info" message={success} onClose={() => setSucces(null)} duration={10000}/>} 
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