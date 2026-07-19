import "./PhotoSlot.css"

interface PhotoSlotProps {
  imageUrl?: string
  onUpload?: () => void
  onDelete?: () => void
}

export default function PhotoSlot({ imageUrl, onUpload, onDelete }: PhotoSlotProps) {
  if (!imageUrl) {
    return (
      <button
        className="PhotoSlot PhotoSlot--empty"
        type="button"
        onClick={onUpload}
        aria-label="Ajouter une photo"
      >
        <span className="PhotoSlot-plus">+</span>
      </button>
    )
  }

  return (
    <div className="PhotoSlot">
      <img src={imageUrl} alt="Photo" className="PhotoSlot-img" />
      <div className="PhotoSlot-actions">
        {onDelete && (
          <button
            className="PhotoSlot-btn PhotoSlot-btn--delete"
            onClick={onDelete}
            type="button"
            aria-label="Supprimer la photo"
          >
            X
          </button>
        )}
      </div>
    </div>
  )
}
