import { useNavigate, useParams } from "react-router-dom"
import Topbar from "../components/Topbar"
import TagChip from "../components/TagChip"
import StatusMessage from "../components/StatusMessage"
import { useAuth } from "../context/AuthContext"
import { useUserProfile } from "../hooks/useUserProfile"
import type { PublicProfile } from "../types/profile"
import "./UserProfile.css"

const GENDER_LABELS: Record<string, string> = {
  male: "Homme", female: "Femme", other: "Autre",
}

const PREFERENCE_LABELS: Record<string, string> = {
  male: "Hommes", female: "Femmes", bisexual: "Bisexuel(le)",
}

/* Consultation de profil : toutes les infos publiques + like/unlike/block/report */
export default function UserProfile() {
  const { id } = useParams()
  const userId = Number(id)
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const { profile, loading, error, feedback, setError, setFeedback, toggleLike, block, report } = useUserProfile(userId)

  if (!isAuthenticated) {
    return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
  }

  const handleBlock = async () => {
    if (!window.confirm("Bloquer ce profil ? Il n'apparaîtra plus dans vos résultats.")) return
    const blocked = await block()
    if (blocked) navigate("/home")
  }

  const handleReport = async () => {
    const reason = window.prompt("Pourquoi signaler ce compte comme faux ?")
    if (reason === null) return
    await report(reason)
  }

  return (
    <div className="app-container page-scroll">
      <Topbar />
      <div className="user-profile">
        {error && <StatusMessage type="error" message={error} onClose={() => setError(null)} />}
        {feedback && <StatusMessage type="success" message={feedback} onClose={() => setFeedback(null)} />}

        {loading && <p>Chargement...</p>}
        {!loading && !profile && <h1>Profil introuvable</h1>}

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

/* En-tête : photo de profil, identité, statut en ligne, badges relation */
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
          {profile.age !== null && <span className="up-age">, {profile.age} ans</span>}
        </h1>
        <p className="up-username">@{profile.username} — {profile.first_name} {profile.last_name}</p>
        <OnlineStatus profile={profile} />
        <div className="up-badges">
          <span className="up-badge">★ {profile.fame_rating} popularité</span>
          {profile.city && <span className="up-badge">{profile.city}</span>}
          {profile.distance_km !== null && (
            <span className="up-badge">{Math.round(profile.distance_km)} km</span>
          )}
        </div>
        <div className="up-badges">
          {profile.connected && <span className="up-badge up-badge-match">Connectés ✓</span>}
          {!profile.connected && profile.likes_me && (
            <span className="up-badge up-badge-like">Ce profil vous a liké</span>
          )}
          {profile.liked_by_me && !profile.connected && (
            <span className="up-badge up-badge-like">Vous avez liké ce profil</span>
          )}
        </div>
      </div>
    </div>
  )
}

/* Statut : en ligne, ou date/heure de dernière connexion (sujet IV.5) */
function OnlineStatus({ profile }: { profile: PublicProfile }) {
  if (profile.is_online) {
    return <p className="up-status up-status-online">● En ligne</p>
  }
  const lastSeen = profile.last_online
    ? new Date(profile.last_online).toLocaleString("fr-FR", {
        day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
      })
    : "inconnue"
  return <p className="up-status">○ Hors ligne — dernière connexion : {lastSeen}</p>
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
      <button className="up-btn" onClick={onBlock}>🚫 Bloquer</button>
      <button className="up-btn" onClick={onReport}>⚠ Signaler</button>
    </div>
  )
}

/* Bio, genre, préférence, tags */
function ProfileDetails({ profile }: { profile: PublicProfile }) {
  return (
    <div className="up-details brutal-card">
      <h2>À propos</h2>
      <p className="up-bio">{profile.biography || "Pas encore de biographie."}</p>
      <div className="up-facts">
        {profile.gender && <p><strong>Genre :</strong> {GENDER_LABELS[profile.gender] ?? profile.gender}</p>}
        {profile.sexual_preference && (
          <p><strong>Recherche :</strong> {PREFERENCE_LABELS[profile.sexual_preference] ?? profile.sexual_preference}</p>
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

/* Galerie de photos */
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
