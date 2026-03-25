import { useRef, type ChangeEvent } from "react"
import PhotoSlot from "../PhotoSlot"
import { uploadPhoto, deletePhoto, setProfilePhoto } from "../../services/profile"
import type { Photo } from "../../types/profile"
import { MAX_PHOTOS, UPLOAD_BASE, ACCEPTED_IMAGE_TYPES } from "../../constants/profile"
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
      onUpdate(photos.filter((p) => p.id !== photoId))
    } catch (e) {
      alert(e instanceof Error ? e.message : "Delete error")
    }
  }

  async function handleSetProfile(photoId: number) {
    try {
      await setProfilePhoto(photoId)
      onUpdate(photos.map((p) => ({ ...p, is_profile: p.id === photoId })))
    } catch (e) {
      alert(e instanceof Error ? e.message : "Error setting profile photo")
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

  const slots = Array.from({ length: MAX_PHOTOS }, (_, i) => photos[i] || null)

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

      <div className="PhotosSection-grid">
        {slots.map((photo, index) => (
          <PhotoSlot
            key={photo ? photo.id : `empty-${index}`}
            imageUrl={photo ? `${UPLOAD_BASE}${photo.file_path}` : undefined}
            isProfile={photo?.is_profile}
            onUpload={!photo && photos.length < MAX_PHOTOS ? triggerUpload : undefined}
            onDelete={photo ? () => handleDelete(photo.id) : undefined}
            onSetProfile={photo ? () => handleSetProfile(photo.id) : undefined}
          />
        ))}
      </div>
    </div>
  )
}
