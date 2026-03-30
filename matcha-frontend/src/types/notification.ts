export interface Notification {
  id: number
  type: "like" | "visit" | "match" | "unlike" | "message"
  is_read: boolean
  created_at: string
  username: string | null
  first_name: string | null
  last_name: string | null
}