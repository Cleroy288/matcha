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
