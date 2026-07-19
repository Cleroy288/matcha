import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { BrowseFilters, SuggestedProfile } from "../types/browse"

/* Sérialise les filtres en query string, en ignorant les champs vides */
export function buildBrowseQuery(filters: BrowseFilters): string {
  const params = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return
    params.set(key, String(value))
  })
  return params.toString()
}

/* Profils suggérés du feed (tri par score par défaut) */
export async function browseProfiles(filters: BrowseFilters): Promise<SuggestedProfile[]> {
  return fetchProfileList(API_ROUTES.browse, filters)
}

/* Recherche avancée (âge, fame, localisation, tags) */
export async function searchProfiles(filters: BrowseFilters): Promise<SuggestedProfile[]> {
  return fetchProfileList(API_ROUTES.search, filters)
}

async function fetchProfileList(baseUrl: string, filters: BrowseFilters): Promise<SuggestedProfile[]> {
  const query = buildBrowseQuery(filters)
  const res = await fetchWithCredentials(query ? `${baseUrl}?${query}` : baseUrl)
  const data = await handleResponse<{ profiles: SuggestedProfile[] }>(res)
  return data.profiles
}
