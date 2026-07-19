import { describe, it, expect } from "vitest"
import { buildBrowseQuery } from "./browse"
import type { BrowseFilters } from "../types/browse"

describe("buildBrowseQuery", () => {
  it("sérialise les filtres numériques et textuels", () => {
    const filters: BrowseFilters = {
      age_min: 20,
      age_max: 35,
      city: "Paris",
      sort_by: "fame",
      order: "desc",
    }
    const query = buildBrowseQuery(filters)
    const params = new URLSearchParams(query)

    expect(params.get("age_min")).toBe("20")
    expect(params.get("age_max")).toBe("35")
    expect(params.get("city")).toBe("Paris")
    expect(params.get("sort_by")).toBe("fame")
    expect(params.get("order")).toBe("desc")
  })

  it("ignore les champs vides, null ou undefined", () => {
    const filters: BrowseFilters = {
      age_min: "",
      city: "",
      fame_min: undefined,
      sort_by: "score",
    }
    const query = buildBrowseQuery(filters)
    const params = new URLSearchParams(query)

    expect(params.has("age_min")).toBe(false)
    expect(params.has("city")).toBe(false)
    expect(params.has("fame_min")).toBe(false)
    expect(params.get("sort_by")).toBe("score")
  })

  it("retourne une chaîne vide sans filtre", () => {
    expect(buildBrowseQuery({})).toBe("")
  })

  it("garde la valeur 0 (filtre légitime)", () => {
    const query = buildBrowseQuery({ min_common_tags: 0 })
    const params = new URLSearchParams(query)

    expect(params.get("min_common_tags")).toBe("0")
  })
})
