import { useCallback, useEffect, useRef, useState } from "react"
import {
  fetchPublicProfile, visitUser, likeUser, unlikeUser, blockUser, reportUser
} from "../services/social"
import type { PublicProfile } from "../types/profile"

/* Logique de la page consultation de profil : chargement + visite + actions sociales */
export function useUserProfile(userId: number) {
  const [profile, setProfile] = useState<PublicProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [feedback, setFeedback] = useState<string | null>(null)
  const visitedRef = useRef<number | null>(null)

  const load = useCallback(async () => {
    setError(null)
    try {
      setProfile(await fetchPublicProfile(userId))
    } catch (e) {
      setError(e instanceof Error ? e.message : "Server error")
    } finally {
      setLoading(false)
    }
  }, [userId])

  // consultation = enregistrée dans l'historique de visites (sujet IV.5)
  useEffect(() => {
    // /user/abc → Number("abc") = NaN : la route backend <int:user_id> ne
    // matche pas, on récupérait un 404 pour rien. La page affiche alors son
    // « Profil introuvable » sans requête réseau.
    if (!Number.isInteger(userId) || userId <= 0) {
      setProfile(null)
      setLoading(false)
      return
    }
    setLoading(true)
    load()

    // StrictMode (dev) démonte/remonte le composant et ré-exécute cet effect ;
    // ce ref survit au remount et évite d'enregistrer 2 visites pour le même userId.
    if (visitedRef.current !== userId) {
      visitedRef.current = userId
      visitUser(userId).catch(() => {})
    }
  }, [userId, load])

  const toggleLike = async () => {
    if (!profile) return
    try {
      if (profile.liked_by_me) {
        await unlikeUser(userId)
        setFeedback("Like removed")
      } else {
        const result = await likeUser(userId)
        setFeedback(result.match ? "It's a match!" : "Profile liked")
      }
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : "Server error")
    }
  }

  const block = async (): Promise<boolean> => {
    try {
      await blockUser(userId)
      return true
    } catch (e) {
      setError(e instanceof Error ? e.message : "Server error")
      return false
    }
  }

  const report = async (reason: string) => {
    try {
      await reportUser(userId, reason)
      setFeedback("Profile reported as a fake account")
    } catch (e) {
      setError(e instanceof Error ? e.message : "Server error")
    }
  }

  return { profile, loading, error, feedback, setError, setFeedback, toggleLike, block, report }
}
