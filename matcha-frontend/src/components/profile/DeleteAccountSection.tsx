import { useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "../Button"
import StatusMessage from "../StatusMessage"
import { useAuth } from "../../context/AuthContext"
import { deleteAccount } from "../../services/profile"
import "./DeleteAccountSection.css"

const CONFIRM_PROMPT = "This will permanently delete your account and all your data. Type DELETE to confirm."
const CONFIRM_WORD = "DELETE"

/* Droit à l'effacement (RGPD art. 17) : suppression définitive du compte et de
   toutes les données personnelles, confirmée par une saisie explicite. */
export default function DeleteAccountSection() {
  const navigate = useNavigate()
  const { setUser } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState(false)

  async function handleDelete() {
    // 1 confirmation par saisie : un simple clic ne doit pas pouvoir tout effacer
    if (window.prompt(CONFIRM_PROMPT) !== CONFIRM_WORD) {
      return
    }

    setError(null)
    setDeleting(true)
    try {
      await deleteAccount()
      setUser(null)
      navigate("/login", { replace: true })
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error deleting account")
      setDeleting(false)
    }
  }

  return (
    <div className="DeleteAccountSection">
      <h3>Delete my account</h3>

      <p className="DeleteAccountSection-notice">
        Deleting your account permanently removes your profile, location, photos,
        tags, likes, profile views, blocks, reports, messages and notifications.
        This cannot be undone.
      </p>

      {error && <StatusMessage type="error" message={error} onClose={() => setError(null)} />}

      <Button onClick={handleDelete} disabled={deleting}>
        {deleting ? "Deleting..." : "Delete my account"}
      </Button>
    </div>
  )
}
