import type { User } from "../types/auth"

export const DEFAULT_ROUTE = "/home"
export const ONBOARDING_ROUTE = "/profile/edit"
export const LOGIN_ROUTE = "/login"

/* Guard rule for a protected route: guests log in first, incomplete profiles finish onboarding. */
export function getProtectedRedirect(user: User | null, requireComplete: boolean) {
  if (!user) return LOGIN_ROUTE
  if (requireComplete && !user.profile_complete) return ONBOARDING_ROUTE
  return null
}

/* Landing route right after a successful login; requestedPath is the page the
   guard bounced away from, so the deep link is not lost. */
export function getPostLoginRoute(user: User, requestedPath?: string | null) {
  if (!user.profile_complete) return ONBOARDING_ROUTE
  return requestedPath || DEFAULT_ROUTE
}
