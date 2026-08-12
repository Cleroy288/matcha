import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { LoginPayload, LoginResponse, RegisterPayload, RegisterResponse } from "../types/auth"

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const res = await fetchWithCredentials(API_ROUTES.login, {
    method: "POST",
    body: JSON.stringify(payload)
  })
  return handleResponse<LoginResponse>(res)
}

export async function register(payload: RegisterPayload): Promise<RegisterResponse> {
  const res = await fetchWithCredentials(API_ROUTES.register, {
    method: "POST",
    body: JSON.stringify(payload)
  })
  return handleResponse<RegisterResponse>(res)
}

export async function verifyEmail(token: string): Promise<{ message: string }> {
  const res = await fetchWithCredentials(`${API_ROUTES.verifyEmail}?token=${token}`)
  return handleResponse<{ message: string }>(res)
}

export async function resetPassword(email: string): Promise<{ message: string }> {
  const res = await fetchWithCredentials(API_ROUTES.resetPassword, {
    method: "POST",
    body: JSON.stringify({ email })
  })
  return handleResponse<{ message: string }>(res)
}

export async function verifyResetPassword(token: string, password: string): Promise<{ message: string }> {
  const res = await fetchWithCredentials(`${API_ROUTES.verifyResetPassword}?token=${token}`, {
    method: "POST",
    body: JSON.stringify({ password })
  })
  return handleResponse<{ message: string }>(res)
}
