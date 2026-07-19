import { useCallback, useEffect, useState } from "react"
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

  const load = useCallback(async () => {
    setError(null)
    try {
      setProfile(await fetchPublicProfile(userId))
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur serveur")
    } finally {
      setLoading(false)
    }
  }, [userId])

  // consultation = enregistrée dans l'historique de visites (sujet IV.5)
  useEffect(() => {
    setLoading(true)
    load()
    visitUser(userId).catch(() => {})
  }, [userId, load])

  const toggleLike = async () => {
    if (!profile) return
    try {
      if (profile.liked_by_me) {
        await unlikeUser(userId)
        setFeedback("Like retiré")
      } else {
        const result = await likeUser(userId)
        setFeedback(result.match ? "C'est un match !" : "Profil liké")
      }
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur serveur")
    }
  }

  const block = async (): Promise<boolean> => {
    try {
      await blockUser(userId)
      return true
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur serveur")
      return false
    }
  }

  const report = async (reason: string) => {
    try {
      await reportUser(userId, reason)
      setFeedback("Profil signalé comme faux compte")
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur serveur")
    }
  }

  return { profile, loading, error, feedback, setError, setFeedback, toggleLike, block, report }
}
