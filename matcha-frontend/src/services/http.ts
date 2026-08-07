const DEFAULT_ERROR_MESSAGE = "Server error"

/* Erreur portée par une réponse HTTP non-2xx, avec son statut.
   Permet aux appelants de distinguer un 401 d'un 400 sans parser le message. */
export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

/* Lit le corps sans jamais laisser fuir un SyntaxError : une réponse d'erreur
   peut être vide ou en HTML (page 413/503 de nginx, page d'erreur Flask). */
async function readJsonBody(res: Response): Promise<unknown> {
  try {
    return await res.json()
  } catch {
    return null
  }
}

/* Extrait le message d'erreur du backend, qui répond toujours {"error": "..."} */
function extractErrorMessage(body: unknown): string | null {
  if (!body || typeof body !== "object" || !("error" in body)) {
    return null
  }
  const { error } = body as { error?: unknown }
  return typeof error === "string" && error.trim() ? error : null
}

/* Parse une réponse API : JSON si ok, sinon jette l'erreur renvoyée par le backend.
   Source unique — ne pas redéfinir cette logique dans les services. */
export async function handleResponse<T>(res: Response): Promise<T> {
  const body = await readJsonBody(res)

  if (!res.ok) {
    throw new ApiError(extractErrorMessage(body) ?? DEFAULT_ERROR_MESSAGE, res.status)
  }

  if (body === null) {
    // 2xx dont le corps n'est pas exploitable : erreur propre plutôt qu'un
    // SyntaxError brut affiché à l'utilisateur
    throw new ApiError(DEFAULT_ERROR_MESSAGE, res.status)
  }

  return body as T
}
