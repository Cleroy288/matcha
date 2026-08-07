import type { Profile, Tag, Photo } from "../types/profile"
import { API_URL } from "../constants/profile"
import { fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"

export async function fetchProfile(): Promise<Profile> {
  const res = await fetchWithCredentials(`${API_URL}/profile`)
  return handleResponse<Profile>(res)
}

export async function fetchUserPhotos(): Promise<Photo[]> {
  const profile = await fetchProfile()
  return profile.photos
}

export async function updateProfile(data: Record<string, unknown>): Promise<Profile> {
  const res = await fetchWithCredentials(`${API_URL}/profile`, {
    method: "PUT",
    body: JSON.stringify(data)
  })
  return handleResponse<Profile>(res)
}

export async function updateLocation(data: {
  latitude: number | null
  longitude: number | null
  city: string
  gps_consent: boolean
}): Promise<{ message: string }> {
  const res = await fetchWithCredentials(`${API_URL}/profile/location`, {
    method: "PUT",
    body: JSON.stringify(data)
  })
  return handleResponse<{ message: string }>(res)
}

/* Droit à l'effacement (RGPD) : supprime le compte et toutes les données liées */
export async function deleteAccount(): Promise<{ message: string }> {
  const res = await fetchWithCredentials(`${API_URL}/profile`, {
    method: "DELETE"
  })
  return handleResponse<{ message: string }>(res)
}

export async function addTag(name: string): Promise<{ tags: Tag[] }> {
  const res = await fetchWithCredentials(`${API_URL}/profile/tags`, {
    method: "POST",
    body: JSON.stringify({ name })
  })
  return handleResponse<{ tags: Tag[] }>(res)
}

export async function removeTag(name: string): Promise<{ tags: Tag[] }> {
  const res = await fetchWithCredentials(`${API_URL}/profile/tags`, {
    method: "DELETE",
    body: JSON.stringify({ name })
  })
  return handleResponse<{ tags: Tag[] }>(res)
}

export async function searchTags(query: string): Promise<{ tags: Tag[] }> {
  const res = await fetchWithCredentials(
    `${API_URL}/tags/search?q=${encodeURIComponent(query)}`
  )
  return handleResponse<{ tags: Tag[] }>(res)
}

export async function uploadPhoto(file: File): Promise<Photo> {
  const formData = new FormData()
  formData.append("photo", file)
  const res = await fetchWithCredentials(`${API_URL}/profile/photos`, {
    method: "POST",
    body: formData
  })
  return handleResponse<Photo>(res)
}

export async function deletePhoto(photoId: number): Promise<{ message: string }> {
  const res = await fetchWithCredentials(`${API_URL}/profile/photos/${photoId}`, {
    method: "DELETE"
  })
  return handleResponse<{ message: string }>(res)
}

export async function setProfilePhoto(photoId: number): Promise<{ message: string }> {
  const res = await fetchWithCredentials(
    `${API_URL}/profile/photos/${photoId}/profile`,
    { method: "PUT" }
  )
  return handleResponse<{ message: string }>(res)
}
