import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { BrowseFilters, SuggestedProfile } from "../types/browse"

/* Serializes the filters into a query string, skipping empty fields */
export function buildBrowseQuery(filters: BrowseFilters): string {
  const params = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return
    params.set(key, String(value))
  })
  return params.toString()
}

/* Suggested feed profiles (sorted by score by default) */
export async function browseProfiles(filters: BrowseFilters): Promise<SuggestedProfile[]> {
  return fetchProfileList(API_ROUTES.browse, filters)
}

/* Advanced search (age, fame, location, tags) */
export async function searchProfiles(filters: BrowseFilters): Promise<SuggestedProfile[]> {
  return fetchProfileList(API_ROUTES.search, filters)
}

async function fetchProfileList(baseUrl: string, filters: BrowseFilters): Promise<SuggestedProfile[]> {
  const query = buildBrowseQuery(filters)
  const res = await fetchWithCredentials(query ? `${baseUrl}?${query}` : baseUrl)
  const data = await handleResponse<{ profiles: SuggestedProfile[] }>(res)
  return data.profiles
}
