import Topbar from "../components/Topbar";
import Input from "../components/Input";
import Button from "../components/Button";
import StatusMessage from "../components/StatusMessage";
import { useResetPassword } from "../hooks/useResetPassword";

export default function ResetPassword() {

    const {email, setEmail, error, setError, success, setSuccess, handleSubmit} = useResetPassword()

    return (
        <div className="app-container">
            <Topbar></Topbar>
            <h1>Reset Password</h1>
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>}
            {success && <StatusMessage type="info" message={success} onClose={() => setSuccess(null)} duration={10000}/>}
            {(error || success) && <div style={{ height: "1rem" }} />}
            <form onSubmit={handleSubmit} className="brutal-card">
                    <Input
                      type="email"
                      placeholder="email"
                      value={email}
                      autoComplete="email"
                      onChange={(e) => setEmail(e.target.value)}
                    />

                    <Button type="submit"> send mail </Button>
                  </form>
        </div>
    )
}
