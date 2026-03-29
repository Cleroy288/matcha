import { fetchWithCredentials, API_ROUTES } from "../config/api"
import type { Notification } from "../types/notification"

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.error || "Erreur serveur")
  }
  return res.json()
}

export async function fetchNotifications(): Promise<{ notifications: Notification[] }> {
  const res = await fetchWithCredentials(API_ROUTES.notifications)
  return handleResponse(res)
}

export async function markNotificationsRead(): Promise<void> {
  await fetchWithCredentials(API_ROUTES.notificationsRead, { method: "PATCH" })
}