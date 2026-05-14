import "./PhotoSlot.css"

interface PhotoSlotProps {
  imageUrl?: string
  onUpload?: () => void
  onDelete?: () => void
}

export default function PhotoSlot({ imageUrl, onUpload, onDelete }: PhotoSlotProps) {
  if (!imageUrl) {
    return (
      <div className="PhotoSlot PhotoSlot--empty" onClick={onUpload}>
        <span className="PhotoSlot-plus">+</span>
      </div>
    )
  }

  return (
    <div className="PhotoSlot">
      <img src={imageUrl} alt="Photo" className="PhotoSlot-img" />
      <div className="PhotoSlot-actions">
        {onDelete && (
          <button className="PhotoSlot-btn PhotoSlot-btn--delete" onClick={onDelete} type="button">
            X
          </button>
        )}
      </div>
    </div>
  )
}
