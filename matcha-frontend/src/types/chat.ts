export interface Conversation {
  user_id: number
  username: string
  first_name: string | null
  last_name: string | null
  is_online: boolean | null
  last_online: string | null
  profile_photo_url: string | null
  last_message: string | null
  last_message_at: string | null
  last_sender_id: number | null
  unread_count: number
}

export interface Message {
  id: number
  sender_id: number
  receiver_id: number
  content: string
  is_read: boolean
  created_at: string
}
