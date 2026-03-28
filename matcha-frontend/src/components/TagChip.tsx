import "./TagChip.css"

interface TagChipProps {
  label: string
  onRemove?: () => void
}

export default function TagChip({ label, onRemove }: TagChipProps) {
  return (
    <span className="TagChip">
      {label}
      {onRemove && (
        <button className="TagChip-remove" onClick={onRemove} type="button">
          X
        </button>
      )}
    </span>
  )
}
