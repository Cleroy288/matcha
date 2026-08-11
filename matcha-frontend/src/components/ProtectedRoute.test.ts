import { describe, expect, it } from "vitest"
import { getPostLoginRoute, getProtectedRedirect } from "../utils/authRoute"
import type { User } from "../types/auth"

const user: User = {
  id: 7,
  username: "ada",
  email: "ada@example.com",
  first_name: "Ada",
  last_name: "Lovelace",
  profile_complete: false,
}

describe("getProtectedRedirect", () => {
  it("redirects guests to login", () => {
    expect(getProtectedRedirect(null, false)).toBe("/login")
  })

  it("redirects incomplete profiles to onboarding", () => {
    expect(getProtectedRedirect(user, true)).toBe("/profile/edit")
  })

  it("allows authenticated users on permitted routes", () => {
    expect(getProtectedRedirect(user, false)).toBeNull()
    expect(getProtectedRedirect({ ...user, profile_complete: true }, true)).toBeNull()
  })
})

describe("getPostLoginRoute", () => {
  const complete: User = { ...user, profile_complete: true }

  it("sends an incomplete profile to onboarding whatever was requested", () => {
    expect(getPostLoginRoute(user, "/chat/42")).toBe("/profile/edit")
  })

  it("restores the page the guard bounced away from", () => {
    expect(getPostLoginRoute(complete, "/chat/42")).toBe("/chat/42")
  })

  it("falls back to home without a requested page", () => {
    expect(getPostLoginRoute(complete)).toBe("/home")
    expect(getPostLoginRoute(complete, "")).toBe("/home")
  })
})
