import { API_ROUTES, fetchWithCredentials } from "../config/api";

const headers = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("token") ?? ""}`,
});

export async function likeUser(userId: number): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.like}/${userId}`, {
    method: "POST",
    headers: headers(),
  });
  if (!res.ok) throw new Error(await res.text());
}

export async function unlikeUser(userId: number): Promise<void> {
  const res = await fetchWithCredentials(`${API_ROUTES.like}/${userId}`, {
    method: "DELETE",
    headers: headers(),
  });
  if (!res.ok) throw new Error(await res.text());
}

export async function visitUser(userId: number): Promise<void> {
  await fetchWithCredentials(`${API_ROUTES.visit}/${userId}`, {
    method: "POST",
    headers: headers(),
  });
}