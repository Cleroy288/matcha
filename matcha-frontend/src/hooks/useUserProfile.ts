import { useCallback, useEffect, useRef, useState } from "react"
import {
  fetchPublicProfile, visitUser, likeUser, unlikeUser, blockUser, reportUser
} from "../services/social"
import type { PublicProfile } from "../types/profile"

/* Profile view page logic: loading + visit tracking + social actions */
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

  // a view is recorded in the visit history (subject IV.5)
  useEffect(() => {
    // /user/abc → Number("abc") = NaN: the backend route <int:user_id> does
    // not match, so we used to fetch a 404 for nothing. The page now shows its
    // "Profile not found" state without any network request.
    if (!Number.isInteger(userId) || userId <= 0) {
      setProfile(null)
      setLoading(false)
      return
    }
    setLoading(true)
    load()

    // StrictMode (dev) unmounts/remounts the component and re-runs this effect;
    // this ref survives the remount and avoids recording 2 visits for the same userId.
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
