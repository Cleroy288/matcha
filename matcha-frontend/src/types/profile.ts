export type Gender = "male" | "female" | "other"
export type SexualPreference = "male" | "female" | "bisexual"

export interface Tag {
  id: number
  name: string
}

export interface Photo {
  id: number
  file_path: string
  is_profile: boolean
  sort_order: number
}

export interface PublicPhoto extends Photo {
  url: string
}

export interface PublicProfile {
  user_id: number
  username: string
  first_name: string | null
  last_name: string | null
  gender: string | null
  sexual_preference: string | null
  biography: string | null
  birth_date: string | null
  age: number | null
  city: string | null
  fame_rating: number
  is_online: boolean
  last_online: string | null
  distance_km: number | null
  tags: Tag[]
  photos: PublicPhoto[]
  profile_photo_url: string | null
  liked_by_me: boolean
  likes_me: boolean
  connected: boolean
}

export interface Profile {
  id: number
  user_id: number
  username: string
  first_name: string
  last_name: string
  email: string
  gender: Gender | null
  sexual_preference: SexualPreference | null
  biography: string | null
  birth_date: string | null
  fame_rating: number
  latitude: number | null
  longitude: number | null
  city: string | null
  gps_consent: boolean
  profile_complete: boolean
  tags: Tag[]
  photos: Photo[]
}
