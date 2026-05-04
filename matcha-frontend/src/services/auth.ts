import { API_ROUTES, fetchWithCredentials } from "../config/api"
import type { LoginPayload, LoginResponse, RegisterPayload } from "../types/auth"

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const res = await fetchWithCredentials(API_ROUTES.login, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}

export async function register(payload: RegisterPayload): Promise<LoginResponse> {
  const res = await fetch(API_ROUTES.register, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}

export async function verifyEmail(token: string): Promise<{ message: string }> {
  const res = await fetch(`${API_ROUTES.verifyEmail}?token=${token}`)
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}

export async function resetPassword(email: string): Promise<{ message: string }> {
  const res = await fetch(API_ROUTES.resetPassword, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}

export async function verifyResetPassword(token: string, password: string): Promise<{ message: string }> {
  const res = await fetch(`${API_ROUTES.verifyResetPassword}?token=${token}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password })
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}