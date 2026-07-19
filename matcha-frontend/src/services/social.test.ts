import { afterEach, describe, expect, it, vi } from "vitest"
import { fetchReceivedLikes, fetchReceivedViews } from "./social"

afterEach(() => vi.unstubAllGlobals())

describe("account activity", () => {
  it("charge les likes et les visites reçus", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ likes: [{ id: 2 }] })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ views: [{ id: 3 }] })))
    vi.stubGlobal("fetch", fetchMock)

    expect(await fetchReceivedLikes()).toEqual([{ id: 2 }])
    expect(await fetchReceivedViews()).toEqual([{ id: 3 }])
    expect(fetchMock.mock.calls[0][0]).toMatch(/\/likes\/received$/)
    expect(fetchMock.mock.calls[1][0]).toMatch(/\/views\/received$/)
  })
})
