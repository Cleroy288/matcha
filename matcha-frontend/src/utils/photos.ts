import { MAX_PHOTOS } from "../constants/profile"
import type { Photo } from "../types/profile"

export function splitPhotos(photos: Photo[]) {
  const primary = photos.find((photo) => photo.is_profile) ?? photos[0] ?? null
  return {
    primary,
    standard: photos.filter((photo) => photo.id !== primary?.id).slice(0, MAX_PHOTOS - 1),
  }
}
