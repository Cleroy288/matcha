import { useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "../Button"
import StatusMessage from "../StatusMessage"
import { useAuth } from "../../context/AuthContext"
import { deleteAccount } from "../../services/profile"
import "./DeleteAccountSection.css"

const CONFIRM_PROMPT = "This will permanently delete your account and all your data. Type DELETE to confirm."
const CONFIRM_WORD = "DELETE"

/* Right to erasure (GDPR art. 17): permanent deletion of the account and of
   every personal record, confirmed by an explicit typed input. */
export default function DeleteAccountSection() {
  const navigate = useNavigate()
  const { setUser } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState(false)

  async function handleDelete() {
    // 1 typed confirmation: a single click must never be able to wipe everything
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
