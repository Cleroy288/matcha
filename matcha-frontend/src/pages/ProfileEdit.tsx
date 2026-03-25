import { useState, useEffect } from "react"
import { useAuth } from "../context/AuthContext"
import Topbar from "../components/Topbar"
import ProfileInfoForm from "../components/profile/ProfileInfoForm"
import TagsSection from "../components/profile/TagsSection"
import PhotosSection from "../components/profile/PhotosSection"
import LocationSection from "../components/profile/LocationSection"
import { fetchProfile } from "../services/profile"
import type { Profile } from "../types/profile"
import "./ProfileEdit.css"

export default function ProfileEdit() {
  const { isAuthenticated } = useAuth()
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!isAuthenticated) return
    loadProfile()
  }, [isAuthenticated])

  async function loadProfile() {
    try {
      const data = await fetchProfile()
      setProfile(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error loading profile")
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="app-container">
        <Topbar />
        <h1>Veuillez vous connecter</h1>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="app-container">
        <Topbar />
        <p>Chargement...</p>
      </div>
    )
  }

  if (error || !profile) {
    return (
      <div className="app-container">
        <Topbar />
        <p>{error || "Erreur de chargement"}</p>
      </div>
    )
  }

  return (
    <div className="app-container">
      <Topbar />
      <div className="ProfileEdit">
        <h1>Mon Profil</h1>

        <div className="ProfileEdit-sections">
          <ProfileInfoForm
            profile={profile}
            onUpdate={(updated) => setProfile(updated)}
          />

          <TagsSection
            tags={profile.tags}
            onUpdate={(tags) => setProfile({ ...profile, tags })}
          />

          <PhotosSection
            photos={profile.photos}
            onUpdate={(photos) => setProfile({ ...profile, photos })}
          />

          <LocationSection
            latitude={profile.latitude}
            longitude={profile.longitude}
            city={profile.city}
            gpsConsent={profile.gps_consent}
            onUpdate={(lat, lng, city, consent) =>
              setProfile({ ...profile, latitude: lat, longitude: lng, city, gps_consent: consent })
            }
          />
        </div>
      </div>
    </div>
  )
}
