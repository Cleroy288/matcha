import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { Conversation, Message } from "../types/chat"

/* Liste des conversations (matchs) avec dernier message et non-lus */
export async function fetchConversations(): Promise<Conversation[]> {
  const res = await fetchWithCredentials(API_ROUTES.chatConversations)
  const data = await handleResponse<{ conversations: Conversation[] }>(res)
  return data.conversations
}

/* Historique d'une conversation ; le backend marque les messages reçus comme lus */
export async function fetchMessages(userId: number): Promise<Message[]> {
  const res = await fetchWithCredentials(`${API_ROUTES.chatMessages}/${userId}`)
  const data = await handleResponse<{ messages: Message[] }>(res)
  return data.messages
}

/* Envoie un message au match et retourne le message créé */
export async function sendMessage(userId: number, content: string): Promise<Message> {
  const res = await fetchWithCredentials(`${API_ROUTES.chatMessages}/${userId}`, {
    method: "POST",
    body: JSON.stringify({ content }),
  })
  return handleResponse<Message>(res)
}

/* Total de messages non lus (badge topbar) */
export async function fetchUnreadMessages(): Promise<number> {
  const res = await fetchWithCredentials(API_ROUTES.chatUnread)
  const data = await handleResponse<{ count: number }>(res)
  return data.count
}
