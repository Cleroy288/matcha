import Topbar from "../components/Topbar"
import Input from "../components/Input"
import Button from "../components/Button"
import StatusMessage from "../components/StatusMessage"
import { useRegister } from "../hooks/useRegister"

export default function Register(){

    const { first_name, setFirstName, last_name, setLastName, email, setEmail,
              username, setUsername, password, setPassword,
              error, setError, success, setSuccess, handleSubmit } = useRegister()
    return (
        <div className="app-container">
            <h1>Register</h1>
            <Topbar></Topbar>
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
            {success && <StatusMessage type="success" message={success} onClose={() => setSuccess(null)}/>} 
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