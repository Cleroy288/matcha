/* Parse une réponse API : JSON si ok, sinon jette l'erreur renvoyée par le backend */
export async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.error || "Erreur serveur")
  }
  return res.json()
}
