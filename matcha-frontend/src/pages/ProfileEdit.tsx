import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import Topbar from "../components/Topbar"
import Button from "../components/Button"
import ProfileInfoForm from "../components/profile/ProfileInfoForm"
import TagsSection from "../components/profile/TagsSection"
import PhotosSection from "../components/profile/PhotosSection"
import LocationSection from "../components/profile/LocationSection"
import AccountActivity from "../components/profile/AccountActivity"
import DeleteAccountSection from "../components/profile/DeleteAccountSection"
import { fetchProfile } from "../services/profile"
import type { Profile } from "../types/profile"
import ThemeSelector from "../components/ThemeSelector"
import "./ProfileEdit.css"

export default function ProfileEdit() {
  const { isAuthenticated, setUser, user } = useAuth()
  const navigate = useNavigate()
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [onboarding, setOnboarding] = useState(false)
  const [finishing, setFinishing] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) return
    loadProfile()
  }, [isAuthenticated])

  async function loadProfile() {
    try {
      const data = await fetchProfile()
      setProfile(data)
      setOnboarding(!data.profile_complete)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error loading profile")
    } finally {
      setLoading(false)
    }
  }

  function handleProfileUpdate(updated: Profile) {
    setProfile(updated)
    if (user) {
      setUser({
        ...user,
        first_name: updated.first_name,
        last_name: updated.last_name,
        email: updated.email,
      })
    }
  }

  async function handleFinish() {
    setError("")
    setFinishing(true)
    try {
      const latest = await fetchProfile()
      setProfile(latest)
      if (!latest.profile_complete) {
        setError("Complete all required fields, add at least 5 tags, a profile photo, and a location")
        return
      }
      setOnboarding(false)
      navigate("/home", { replace: true })
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error checking profile")
    } finally {
      setFinishing(false)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="app-container">
        <Topbar />
        <h1>Please log in</h1>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="app-container">
        <Topbar />
        <p>Loading...</p>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="app-container">
        <Topbar />
        <p>{error || "Loading error"}</p>
      </div>
    )
  }

  return (
    <div className="app-container page-scroll">
      <Topbar />
      <ThemeSelector></ThemeSelector>
      <div className="ProfileEdit">
        <h1>{onboarding ? "Complete your profile" : "My profile"}</h1>
        {error && <p>{error}</p>}
        <div className="fame-rating">
        ⭐ Fame rating: <strong>{profile.fame_rating ?? 0} / 10</strong>
        </div>

        <div className="ProfileEdit-sections">
          <ProfileInfoForm
            profile={profile}
            onUpdate={handleProfileUpdate}
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

          {!onboarding && <AccountActivity />}
          {!onboarding && <DeleteAccountSection />}

          {onboarding && (
            <Button onClick={handleFinish} disabled={finishing}>
              {finishing ? "Checking..." : "Finish registration"}
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
