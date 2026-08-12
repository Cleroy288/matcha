import { useEffect, useState } from "react"
import { useAuth } from "../context/AuthContext"
import Topbar from "../components/Topbar"
import PhotosSection from "../components/profile/PhotosSection"
import { fetchUserPhotos } from "../services/profile"
import type { Photo } from "../types/profile"

export default function Profile() {
  const { user, isAuthenticated } = useAuth()
  const [photos, setPhotos] = useState<Photo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!isAuthenticated) return

    loadPhotos()
  }, [isAuthenticated])

  async function loadPhotos() {
    try {
      const data = await fetchUserPhotos()
      setPhotos(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error loading photos")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="app-container">
        <Topbar />
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="app-container">
        <Topbar></Topbar>
      <div className="brutal-card" style={{ background: "var(--accent)" }}>
        <h1>My profile</h1>
        <hr style={{ borderWidth: "3px", borderColor: "black" }} />
        
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <p><strong>ID:</strong> {user?.id}</p>
          <p><strong>Username:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>First name:</strong> {user?.first_name || "Not set"}</p>
          <p><strong>Last name:</strong> {user?.last_name || "Not set"}</p>
        </div>

        {error && <p>{error}</p>}

        <div style={{ marginTop: "20px" }}>
          <PhotosSection
            photos={photos}
            onUpdate={setPhotos}
          />
        </div>
      </div>
    </div>
  )
}
