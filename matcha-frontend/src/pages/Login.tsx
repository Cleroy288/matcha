import Button from "../components/Button.tsx"
import Input from "../components/Input.tsx"
import Topbar from "../components/Topbar.tsx"
import { Link } from "react-router-dom"
import StatusMessage from "../components/StatusMessage.tsx"

import TwoCoeur from "../assets/doublecoeur.svg?react"
import Couple from "../assets/cup2.svg?react"
import Cup4 from "../assets/cup4.svg?react"
import Cupi from "../assets/coeurcupidon.svg?react"
import CupTchin from "../assets/cupTchin.svg?react"
import OiseauVol from "../assets/oiseauCoeur.svg?react"
import { useLogin } from "../hooks/useLogin.ts"


export default function Login() {
  const { username, setUsername, password, setPassword,
          error, setError, success, setSuccess, handleSubmit } = useLogin()

  return (
    <div className="app-container page-scroll">
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
      {success && <StatusMessage type="success" message={success} onClose={() => setSuccess(null)}/>}
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
