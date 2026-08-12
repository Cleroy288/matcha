import type { SuggestedProfile } from "../types/browse"
import type { ProfileCardData } from "../components/ProfileCard"

/* Adapts a suggested profile (API) to the tinder card format */
export function toCardData(profile: SuggestedProfile): ProfileCardData {
  const photoUrls = profile.photo_urls?.length
    ? profile.photo_urls
    : profile.profile_photo_url
      ? [profile.profile_photo_url]
      : []

  return {
    userId: profile.user_id,
    name: profile.first_name ?? profile.username,
    age: profile.age,
    distance: profile.distance_km,
    photoUrls,
    city: profile.city,
    fame: profile.fame_rating,
    commonTags: profile.common_tags,
    isOnline: profile.is_online ?? false,
  }
}
