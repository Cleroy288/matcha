const DEFAULT_ERROR_MESSAGE = "Server error"

/* Error carried by a non-2xx HTTP response, along with its status.
   Lets callers tell a 401 from a 400 without parsing the message. */
export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

/* Reads the body without ever leaking a SyntaxError: an error response can be
   empty or in HTML (nginx 413/503 page, Flask error page). */
async function readJsonBody(res: Response): Promise<unknown> {
  try {
    return await res.json()
  } catch {
    return null
  }
}

/* Extracts the backend error message, which is always {"error": "..."} */
function extractErrorMessage(body: unknown): string | null {
  if (!body || typeof body !== "object" || !("error" in body)) {
    return null
  }
  const { error } = body as { error?: unknown }
  return typeof error === "string" && error.trim() ? error : null
}

/* Parses an API response: JSON when ok, otherwise throws the backend error.
   Single source of truth — do not redefine this logic in the services. */
export async function handleResponse<T>(res: Response): Promise<T> {
  const body = await readJsonBody(res)

  if (!res.ok) {
    throw new ApiError(extractErrorMessage(body) ?? DEFAULT_ERROR_MESSAGE, res.status)
  }

  if (body === null) {
    // 2xx whose body cannot be used: a clean error rather than a raw
    // SyntaxError shown to the user
    throw new ApiError(DEFAULT_ERROR_MESSAGE, res.status)
  }

  return body as T
}
