export type SortKey = "score" | "age" | "distance" | "fame" | "common_tags"
export type SortOrder = "asc" | "desc"

export interface SuggestedProfile {
  user_id: number
  username: string
  first_name: string | null
  last_name: string | null
  gender: string | null
  sexual_preference: string | null
  city: string | null
  fame_rating: number
  is_online: boolean
  last_online: string | null
  age: number
  common_tags: number
  distance_km: number | null
  profile_photo_url: string | null
  photo_urls: string[]
}

export interface BrowseFilters {
  age_min?: number | ""
  age_max?: number | ""
  fame_min?: number | ""
  fame_max?: number | ""
  distance_max?: number | ""
  min_common_tags?: number | ""
  city?: string
  tags?: string
  sort_by?: SortKey
  order?: SortOrder
}
