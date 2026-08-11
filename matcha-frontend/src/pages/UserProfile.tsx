import { useNavigate, useParams } from "react-router-dom"
import Topbar from "../components/Topbar"
import TagChip from "../components/TagChip"
import StatusMessage from "../components/StatusMessage"
import { useUserProfile } from "../hooks/useUserProfile"
import type { PublicProfile } from "../types/profile"
import "./UserProfile.css"

const GENDER_LABELS: Record<string, string> = {
  male: "Man", female: "Woman", other: "Other",
}

const PREFERENCE_LABELS: Record<string, string> = {
  male: "Men", female: "Women", bisexual: "Both",
}

/* Profile view: every public field + like/unlike/block/report */
export default function UserProfile() {
  const { id } = useParams()
  const userId = Number(id)
  const navigate = useNavigate()
  const { profile, loading, error, feedback, setError, setFeedback, toggleLike, block, report } = useUserProfile(userId)

  const handleBlock = async () => {
    if (!window.confirm("Block this profile? It will no longer appear in your results.")) return
    const blocked = await block()
    if (blocked) navigate("/home")
  }

  const handleReport = async () => {
    const reason = window.prompt("Why are you reporting this account as fake?")
    if (reason === null) return
    await report(reason)
  }

  return (
    <div className="app-container page-scroll">
      <Topbar />
      <div className="user-profile">
        {error && <StatusMessage type="error" message={error} onClose={() => setError(null)} />}
        {feedback && <StatusMessage type="success" message={feedback} onClose={() => setFeedback(null)} />}

        {loading && <p>Loading...</p>}
        {!loading && !profile && <h1>Profile not found</h1>}

        {profile && (
          <>
            <ProfileHeader profile={profile} />
            <ProfileActions
              profile={profile}
              onToggleLike={toggleLike}
              onChat={() => navigate(`/chat/${userId}`)}
              onBlock={handleBlock}
              onReport={handleReport}
            />
            <ProfileDetails profile={profile} />
            <ProfilePhotos profile={profile} />
          </>
        )}
      </div>
    </div>
  )
}

/* Header: profile photo, identity, online status, relation badges */
function ProfileHeader({ profile }: { profile: PublicProfile }) {
  return (
    <div className="up-header brutal-card">
      <div className="up-photo-wrap">
        {profile.profile_photo_url ? (
          <img className="up-photo" src={profile.profile_photo_url} alt={profile.username} />
        ) : (
          <div className="up-photo up-photo-placeholder">👤</div>
        )}
      </div>
      <div className="up-identity">
        <h1 className="up-name">
          {profile.first_name ?? profile.username}
          {profile.age !== null && <span className="up-age">, {profile.age} y/o</span>}
        </h1>
        <p className="up-username">@{profile.username} — {profile.first_name} {profile.last_name}</p>
        <OnlineStatus profile={profile} />
        <div className="up-badges">
          <span className="up-badge">★ {profile.fame_rating} fame</span>
          {profile.city && <span className="up-badge">{profile.city}</span>}
          {profile.distance_km !== null && (
            <span className="up-badge">{Math.round(profile.distance_km)} km</span>
          )}
        </div>
        <div className="up-badges">
          {profile.connected && <span className="up-badge up-badge-match">Matched ✓</span>}
          {!profile.connected && profile.likes_me && (
            <span className="up-badge up-badge-like">This profile liked you</span>
          )}
          {profile.liked_by_me && !profile.connected && (
            <span className="up-badge up-badge-like">You liked this profile</span>
          )}
        </div>
      </div>
    </div>
  )
}

/* Status: online, or date/time of the last connection (subject IV.5) */
function OnlineStatus({ profile }: { profile: PublicProfile }) {
  if (profile.is_online) {
    return <p className="up-status up-status-online">● Online</p>
  }
  const lastSeen = profile.last_online
    ? new Date(profile.last_online).toLocaleString("en-GB", {
        day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
      })
    : "unknown"
  return <p className="up-status">○ Offline — last seen: {lastSeen}</p>
}

interface ProfileActionsProps {
  profile: PublicProfile
  onToggleLike: () => void
  onChat: () => void
  onBlock: () => void
  onReport: () => void
}

/* Boutons like / unlike / chat / block / report */
function ProfileActions({ profile, onToggleLike, onChat, onBlock, onReport }: ProfileActionsProps) {
  return (
    <div className="up-actions">
      <button className="up-btn up-btn-like" onClick={onToggleLike}>
        {profile.liked_by_me ? "💔 Unlike" : "♥ Like"}
      </button>
      {profile.connected && (
        <button className="up-btn up-btn-chat" onClick={onChat}>💬 Chat</button>
      )}
      <button className="up-btn" onClick={onBlock}>🚫 Block</button>
      <button className="up-btn" onClick={onReport}>⚠ Report</button>
    </div>
  )
}

/* Bio, gender, preference, tags */
function ProfileDetails({ profile }: { profile: PublicProfile }) {
  return (
    <div className="up-details brutal-card">
      <h2>About</h2>
      <p className="up-bio">{profile.biography || "No biography yet."}</p>
      <div className="up-facts">
        {profile.gender && <p><strong>Gender:</strong> {GENDER_LABELS[profile.gender] ?? profile.gender}</p>}
        {profile.sexual_preference && (
          <p><strong>Looking for:</strong> {PREFERENCE_LABELS[profile.sexual_preference] ?? profile.sexual_preference}</p>
        )}
      </div>
      {profile.tags.length > 0 && (
        <div className="up-tags">
          {profile.tags.map(tag => <TagChip key={tag.id} label={tag.name} />)}
        </div>
      )}
    </div>
  )
}

/* Photo gallery */
function ProfilePhotos({ profile }: { profile: PublicProfile }) {
  if (profile.photos.length === 0) return null
  return (
    <div className="up-photos brutal-card">
      <h2>Photos</h2>
      <div className="up-photos-grid">
        {profile.photos.map(photo => (
          <img key={photo.id} className="up-photo-item" src={photo.url} alt="" />
        ))}
      </div>
    </div>
  )
}
