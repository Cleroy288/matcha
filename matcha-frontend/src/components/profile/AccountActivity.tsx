import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import {
  fetchReceivedLikes,
  fetchReceivedViews,
  type ProfileView,
  type ReceivedLike,
} from "../../services/social"
import "./AccountActivity.css"

export default function AccountActivity() {
  const [likes, setLikes] = useState<ReceivedLike[]>([])
  const [views, setViews] = useState<ProfileView[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    Promise.all([fetchReceivedLikes(), fetchReceivedViews()])
      .then(([receivedLikes, receivedViews]) => {
        setLikes(receivedLikes)
        setViews(receivedViews)
      })
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Impossible de charger l'activité")
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <section className="AccountActivity">
      <h3>Account activity</h3>

      {loading && <p>Chargement...</p>}
      {error && <p className="AccountActivity-error">{error}</p>}

      {!loading && !error && (
        <div className="AccountActivity-columns">
          <ActivityList title="Likes reçus" entries={likes.map(like => ({
            ...like,
            date: like.liked_at,
          }))} />
          <ActivityList title="Visites du profil" entries={views.map(view => ({
            ...view,
            date: view.viewed_at,
          }))} />
        </div>
      )}
    </section>
  )
}

interface ActivityEntry {
  id: number
  username: string
  first_name: string | null
  last_name: string | null
  date: string
}

function ActivityList({ title, entries }: { title: string; entries: ActivityEntry[] }) {
  return (
    <div className="AccountActivity-column">
      <h4>{title} <span>{entries.length}</span></h4>
      {entries.length === 0 ? (
        <p className="AccountActivity-empty">Aucune activité</p>
      ) : (
        <ul className="AccountActivity-list">
          {entries.map((entry, index) => (
            <li key={`${entry.id}-${entry.date}-${index}`}>
              <Link to={`/user/${entry.id}`}>
                <strong>{displayName(entry)}</strong>
                <span>@{entry.username}</span>
              </Link>
              <time dateTime={entry.date}>{formatDate(entry.date)}</time>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function displayName(entry: ActivityEntry): string {
  return `${entry.first_name ?? ""} ${entry.last_name ?? ""}`.trim() || entry.username
}

function formatDate(value: string): string {
  return new Date(value).toLocaleString("fr-FR", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  })
}
