interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

interface LoginResponse {
  token: string
  user: User
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const res = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.error || "Erreur lors du login")
  }
  return res.json()
}