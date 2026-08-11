import { API_ROUTES, fetchWithCredentials } from "../config/api"
import { handleResponse } from "./http"
import type { Conversation, Message } from "../types/chat"

/* Conversation list (matches) with last message and unread count */
export async function fetchConversations(): Promise<Conversation[]> {
  const res = await fetchWithCredentials(API_ROUTES.chatConversations)
  const data = await handleResponse<{ conversations: Conversation[] }>(res)
  return data.conversations
}

/* History of a conversation; the backend marks the received messages as read */
export async function fetchMessages(userId: number): Promise<Message[]> {
  const res = await fetchWithCredentials(`${API_ROUTES.chatMessages}/${userId}`)
  const data = await handleResponse<{ messages: Message[] }>(res)
  return data.messages
}

/* Sends a message to the match and returns the created message */
export async function sendMessage(userId: number, content: string): Promise<Message> {
  const res = await fetchWithCredentials(`${API_ROUTES.chatMessages}/${userId}`, {
    method: "POST",
    body: JSON.stringify({ content }),
  })
  return handleResponse<Message>(res)
}

/* Total unread messages (topbar badge) */
export async function fetchUnreadMessages(): Promise<number> {
  const res = await fetchWithCredentials(API_ROUTES.chatUnread)
  const data = await handleResponse<{ count: number }>(res)
  return data.count
}
