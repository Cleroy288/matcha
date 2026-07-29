import { fetchWithCredentials, API_ROUTES } from "../config/api"
import { handleResponse } from "./http"
import type { Notification } from "../types/notification"

export async function fetchNotifications(): Promise<{ notifications: Notification[] }> {
  const res = await fetchWithCredentials(API_ROUTES.notifications)
  return handleResponse(res)
}

export async function markNotificationsRead(): Promise<void> {
  const res = await fetchWithCredentials(API_ROUTES.notificationsRead, { method: "PATCH" })
  await handleResponse<{ ok: boolean }>(res)
}
