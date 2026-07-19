export interface LoginPayload {
  username: string
  password: string
}

export interface LoginResponse {
    user: User
    message: string
}

export interface RegisterResponse {
    message: string
    email_verification_required: boolean
}

export interface RegisterPayload {
    first_name: string
    last_name: string
    email: string
    username: string
    password: string
    confirm_password: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}
