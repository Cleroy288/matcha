import "./PhotoSlot.css"

interface PhotoSlotProps {
  imageUrl?: string
  isProfile?: boolean
  onUpload?: () => void
  onDelete?: () => void
  onSetProfile?: () => void
}

export default function PhotoSlot({ imageUrl, isProfile, onUpload, onDelete, onSetProfile }: PhotoSlotProps) {
  if (!imageUrl) {
    return (
      <div className="PhotoSlot PhotoSlot--empty" onClick={onUpload}>
        <span className="PhotoSlot-plus">+</span>
      </div>
    )
  }

  return (
    <div className={`PhotoSlot ${isProfile ? "PhotoSlot--profile" : ""}`}>
      <img src={imageUrl} alt="Photo" className="PhotoSlot-img" />
      <div className="PhotoSlot-actions">
        {onSetProfile && !isProfile && (
          <button className="PhotoSlot-btn" onClick={onSetProfile} type="button">
            ★
          </button>
        )}
        {onDelete && (
          <button className="PhotoSlot-btn PhotoSlot-btn--delete" onClick={onDelete} type="button">
            X
          </button>
        )}
      </div>
    </div>
  )
}
