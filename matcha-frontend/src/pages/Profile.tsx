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

  if (!isAuthenticated) {
    return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
  }

  if (loading) {
    return (
      <div className="app-container">
        <Topbar />
        <p>Chargement...</p>
      </div>
    )
  }

  return (
    <div className="app-container">
        <Topbar></Topbar>
      <div className="brutal-card" style={{ background: "var(--accent)" }}>
        <h1>Mon Profil</h1>
        <hr style={{ borderWidth: "3px", borderColor: "black" }} />
        
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <p><strong>ID :</strong> {user?.id}</p>
          <p><strong>Username :</strong> {user?.username}</p>
          <p><strong>Email :</strong> {user?.email}</p>
          <p><strong>Prénom :</strong> {user?.first_name || "Non renseigné"}</p>
          <p><strong>Nom :</strong> {user?.last_name || "Non renseigné"}</p>
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
