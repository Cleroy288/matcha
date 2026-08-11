import { Navigate, Outlet, useLocation } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { getProtectedRedirect, LOGIN_ROUTE } from "../utils/authRoute"

export default function ProtectedRoute({ requireComplete = false }: { requireComplete?: boolean }) {
  const { user, authLoading } = useAuth()
  const location = useLocation()

  // 1 the /me call is still running: redirecting now would log out a valid session
  if (authLoading) return null

  const redirect = getProtectedRedirect(user, requireComplete)
  if (!redirect) return <Outlet />

  // 2 only the login bounce carries the deep link, onboarding always ends on /home
  const state = redirect === LOGIN_ROUTE ? { from: location.pathname + location.search } : undefined
  return <Navigate to={redirect} state={state} replace />
}
