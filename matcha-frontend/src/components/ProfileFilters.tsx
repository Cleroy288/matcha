import { useState } from "react"
import type { BrowseFilters, SortKey, SortOrder } from "../types/browse"
import Input from "./Input"
import Select from "./Select"
import Button from "./Button"
import "./ProfileFilters.css"

interface ProfileFiltersProps {
  variant: "browse" | "search"
  filters: BrowseFilters
  onChange: (filters: BrowseFilters) => void
  onApply: () => void
}

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: "score", label: "Pertinence" },
  { key: "age", label: "Âge" },
  { key: "distance", label: "Distance" },
  { key: "fame", label: "Popularité" },
  { key: "common_tags", label: "Tags communs" },
]

/* Panneau tri + filtres partagé entre le feed (browse) et la recherche avancée */
export default function ProfileFilters({ variant, filters, onChange, onApply }: ProfileFiltersProps) {
  const [open, setOpen] = useState(false)

  const setNumber = (field: keyof BrowseFilters) => (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({ ...filters, [field]: e.target.value === "" ? "" : Number(e.target.value) })
  }

  const setText = (field: keyof BrowseFilters) => (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({ ...filters, [field]: e.target.value })
  }

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    onApply()
  }

  return (
    <div className="filters-panel">
      <button className="filters-toggle" onClick={() => setOpen(!open)} type="button">
        {open ? "▲ Masquer les filtres" : "▼ Filtres & tri"}
      </button>

      {open && (
        <form className="filters-form" onSubmit={submit}>
          <div className="filters-grid">
            <label className="filters-field">
              Âge min
              <Input type="number" min={18} value={filters.age_min ?? ""} onChange={setNumber("age_min")} />
            </label>
            <label className="filters-field">
              Âge max
              <Input type="number" min={18} value={filters.age_max ?? ""} onChange={setNumber("age_max")} />
            </label>
            <label className="filters-field">
              Popularité min
              <Input type="number" min={0} max={10} value={filters.fame_min ?? ""} onChange={setNumber("fame_min")} />
            </label>
            <label className="filters-field">
              Popularité max
              <Input type="number" min={0} max={10} value={filters.fame_max ?? ""} onChange={setNumber("fame_max")} />
            </label>
            <label className="filters-field">
              Distance max (km)
              <Input type="number" min={0} value={filters.distance_max ?? ""} onChange={setNumber("distance_max")} />
            </label>

            {variant === "browse" && (
              <label className="filters-field">
                Tags communs min
                <Input type="number" min={0} value={filters.min_common_tags ?? ""} onChange={setNumber("min_common_tags")} />
              </label>
            )}

            {variant === "search" && (
              <>
                <label className="filters-field">
                  Ville
                  <Input type="text" placeholder="Paris" value={filters.city ?? ""} onChange={setText("city")} />
                </label>
                <label className="filters-field">
                  Tags (séparés par des virgules)
                  <Input type="text" placeholder="#geek,#vegan" value={filters.tags ?? ""} onChange={setText("tags")} />
                </label>
              </>
            )}

            <label className="filters-field">
              Trier par
              <Select
                value={filters.sort_by ?? "score"}
                onChange={(e) => onChange({ ...filters, sort_by: e.target.value as SortKey })}
              >
                {SORT_OPTIONS.map(({ key, label }) => (
                  <option key={key} value={key}>{label}</option>
                ))}
              </Select>
            </label>
            <label className="filters-field">
              Ordre
              <Select
                value={filters.order ?? ""}
                onChange={(e) => onChange({ ...filters, order: (e.target.value || undefined) as SortOrder | undefined })}
              >
                <option value="">Auto</option>
                <option value="asc">Croissant</option>
                <option value="desc">Décroissant</option>
              </Select>
            </label>
          </div>

          <Button type="submit">
            {variant === "search" ? "Rechercher" : "Appliquer"}
          </Button>
        </form>
      )}
    </div>
  )
}
