import Topbar from "../components/Topbar"
import Input from "../components/Input"
import Button from "../components/Button"
import StatusMessage from "../components/StatusMessage"
import { useVerifyResetPassword } from "../hooks/useVerifyResetPassword"

export default function VerifyResetPassword() {
  const { password, setPassword, error, setError, success, setSuccess, handleSubmit } = useVerifyResetPassword()

  return (
    <div className="app-container">
      <Topbar />
      <h1>New password</h1>
      {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>}
      {success && <StatusMessage type="success" message={success} onClose={() => setSuccess(null)}/>}
      {(error || success) && <div style={{ height: "1rem" }} />}
      <form onSubmit={handleSubmit} className="brutal-card">
        <Input
          type="password"
          placeholder="New Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit">Change password</Button>
      </form>
    </div>
  )
}
