import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { PublicProfile } from "../types/profile"

export interface ReceivedLike {
  id: number
  username: string
  first_name: string | null
  last_name: string | null
  liked_at: string
}

export interface ProfileView {
  id: number
  username: string
  first_name: string | null
  last_name: string | null
  viewed_at: string
}

export async function likeUser(userId: number): Promise<{ liked: boolean; match: boolean }> {
  const res = await fetchWithCredentials(`${API_ROUTES.like}/${userId}`, { method: "POST" })
  return handleResponse(res)
}

export async function unlikeUser(userId: number): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.like}/${userId}`, { method: "DELETE" })
  await handleResponse(res)
}

export async function visitUser(userId: number): Promise<void> {
  await fetchWithCredentials(`${API_ROUTES.visit}/${userId}`, { method: "POST" })
}

export async function blockUser(userId: number): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.block}/${userId}`, { method: "POST" })
  await handleResponse(res)
}

export async function unblockUser(userId: number): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.block}/${userId}`, { method: "DELETE" })
  await handleResponse(res)
}

export async function reportUser(userId: number, reason: string): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.report}/${userId}`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  })
  await handleResponse(res)
}

/* Profil public d'un autre user (toutes infos sauf email/mdp + relation like/match) */
export async function fetchPublicProfile(userId: number): Promise<PublicProfile> {
  const res = await fetchWithCredentials(`${API_ROUTES.profile}/${userId}`)
  return handleResponse(res)
}

export async function fetchReceivedLikes(): Promise<ReceivedLike[]> {
  const res = await fetchWithCredentials(API_ROUTES.likesReceived)
  const data = await handleResponse<{ likes: ReceivedLike[] }>(res)
  return data.likes
}

export async function fetchReceivedViews(): Promise<ProfileView[]> {
  const res = await fetchWithCredentials(API_ROUTES.viewsReceived)
  const data = await handleResponse<{ views: ProfileView[] }>(res)
  return data.views
}
