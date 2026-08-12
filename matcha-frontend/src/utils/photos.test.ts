import { expect, it } from "vitest"
import type { Photo } from "../types/profile"
import { splitPhotos } from "./photos"

it("separates the primary photo from the four standard photos", () => {
  const photos: Photo[] = [1, 2, 3, 4, 5].map((id) => ({
    id,
    file_path: `${id}.jpg`,
    is_profile: id === 3,
    sort_order: id - 1,
  }))

  const { primary, standard } = splitPhotos(photos)

  expect(primary?.id).toBe(3)
  expect(standard.map((photo) => photo.id)).toEqual([1, 2, 4, 5])
})
