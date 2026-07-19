import { describe, it, expect } from "vitest"
import { toCardData } from "./profileCard"
import type { SuggestedProfile } from "../types/browse"

const baseProfile: SuggestedProfile = {
  user_id: 42,
  username: "jdoe",
  first_name: "Jane",
  last_name: "Doe",
  gender: "female",
  sexual_preference: "bisexual",
  city: "Lyon",
  fame_rating: 7.5,
  is_online: true,
  last_online: null,
  age: 28,
  common_tags: 3,
  distance_km: 12.7,
  profile_photo_url: "http://localhost/uploads/1.jpg",
  photo_urls: ["http://localhost/uploads/1.jpg", "http://localhost/uploads/2.jpg"],
}

describe("toCardData", () => {
  it("mappe un profil suggéré vers la card", () => {
    const card = toCardData(baseProfile)

    expect(card.userId).toBe(42)
    expect(card.name).toBe("Jane")
    expect(card.age).toBe(28)
    expect(card.distance).toBe(12.7)
    expect(card.photoUrls).toEqual([
      "http://localhost/uploads/1.jpg",
      "http://localhost/uploads/2.jpg",
    ])
    expect(card.city).toBe("Lyon")
    expect(card.fame).toBe(7.5)
    expect(card.commonTags).toBe(3)
    expect(card.isOnline).toBe(true)
  })

  it("retombe sur le username sans prénom", () => {
    const card = toCardData({ ...baseProfile, first_name: null })

    expect(card.name).toBe("jdoe")
  })

  it("gère l'absence de photo et de distance", () => {
    const card = toCardData({ ...baseProfile, profile_photo_url: null, photo_urls: [], distance_km: null })

    expect(card.photoUrls).toEqual([])
    expect(card.distance).toBeNull()
  })
})
