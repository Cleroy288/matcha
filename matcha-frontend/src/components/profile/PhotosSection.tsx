import { useRef, type ChangeEvent } from "react"
import PhotoSlot from "../PhotoSlot"
import { deletePhoto, fetchUserPhotos, setProfilePhoto, uploadPhoto } from "../../services/profile"
import type { Photo } from "../../types/profile"
import { MAX_PHOTOS, UPLOAD_BASE, ACCEPTED_IMAGE_TYPES } from "../../constants/profile"
import { splitPhotos } from "../../utils/photos"
import "./PhotosSection.css"

interface PhotosSectionProps {
  photos: Photo[]
  onUpdate: (photos: Photo[]) => void
}

export default function PhotosSection({ photos, onUpdate }: PhotosSectionProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  async function handleUpload(file: File) {
    try {
      const newPhoto = await uploadPhoto(file)
      onUpdate([...photos, newPhoto])
    } catch (e) {
      alert(e instanceof Error ? e.message : "Upload error")
    }
  }

  async function handleDelete(photoId: number) {
    try {
      await deletePhoto(photoId)
      onUpdate(await fetchUserPhotos())
    } catch (e) {
      alert(e instanceof Error ? e.message : "Delete error")
    }
  }

  async function handleSetPrimary(photoId: number) {
    try {
      await setProfilePhoto(photoId)
      onUpdate(photos.map((photo) => ({ ...photo, is_profile: photo.id === photoId })))
    } catch (e) {
      alert(e instanceof Error ? e.message : "Update error")
    }
  }

  function triggerUpload() {
    fileInputRef.current?.click()
  }

  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (file) handleUpload(file)
    e.target.value = ""
  }

  const { primary, standard } = splitPhotos(photos)
  const standardSlots = Array.from({ length: MAX_PHOTOS - 1 }, (_, i) => standard[i] || null)
  const canUpload = photos.length < MAX_PHOTOS

  return (
    <div className="PhotosSection">
      <h3>Photos ({photos.length}/{MAX_PHOTOS})</h3>

      <input
        ref={fileInputRef}
        type="file"
        accept={ACCEPTED_IMAGE_TYPES}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <section className="PhotosSection-group PhotosSection-main">
        <h4>Photo principale</h4>
        <PhotoSlot
          imageUrl={primary ? `${UPLOAD_BASE}${primary.file_path}` : undefined}
          onUpload={!primary && canUpload ? triggerUpload : undefined}
          onDelete={primary ? () => handleDelete(primary.id) : undefined}
        />
      </section>

      <section className="PhotosSection-group PhotosSection-standard">
        <h4>Photos supplémentaires ({standard.length}/{MAX_PHOTOS - 1})</h4>
        <div className="PhotosSection-grid">
          {standardSlots.map((photo, index) => (
            <div className="PhotosSection-item" key={photo ? photo.id : `empty-${index}`}>
              <PhotoSlot
                imageUrl={photo ? `${UPLOAD_BASE}${photo.file_path}` : undefined}
                onUpload={!photo && canUpload ? triggerUpload : undefined}
                onDelete={photo ? () => handleDelete(photo.id) : undefined}
              />
              {photo && (
                <button
                  className="PhotosSection-primaryButton"
                  type="button"
                  onClick={() => handleSetPrimary(photo.id)}
                >
                  Rendre principale
                </button>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
