// frontend/src/config/api.ts  ← fichier dédié
export const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:5000"

export const API_ROUTES = {
    login:               `${API_BASE_URL}/login`,
    register:            `${API_BASE_URL}/register`,
    logout:              `${API_BASE_URL}/logout`,
    verifyEmail:         `${API_BASE_URL}/verify-email`,
    resetPassword:       `${API_BASE_URL}/reset-password`,
    verifyResetPassword: `${API_BASE_URL}/verify-reset-password`,
    notifications:       `${API_BASE_URL}/notifications`,
    notificationsRead:   `${API_BASE_URL}/notifications/read`,
    notificationsUnread: `${API_BASE_URL}/notifications/unread`,
    like:    `${API_BASE_URL}/like`,
    visit:   `${API_BASE_URL}/visit`,
    block:   `${API_BASE_URL}/block`,
    me:                  `${API_BASE_URL}/me`,
}

export const fetchWithCredentials = (url: string, options: RequestInit = {}) => {
    return fetch(url, {
        ...options,
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        }
    })
}