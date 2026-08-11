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
  { key: "score", label: "Relevance" },
  { key: "age", label: "Age" },
  { key: "distance", label: "Distance" },
  { key: "fame", label: "Fame rating" },
  { key: "common_tags", label: "Common tags" },
]

/* Sort + filter panel shared by the feed (browse) and the advanced search */
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
        {open ? "▲ Hide filters" : "▼ Filters & sorting"}
      </button>

      {open && (
        <form className="filters-form" onSubmit={submit}>
          <div className="filters-grid">
            <label className="filters-field">
              Min age
              <Input type="number" min={18} value={filters.age_min ?? ""} onChange={setNumber("age_min")} />
            </label>
            <label className="filters-field">
              Max age
              <Input type="number" min={18} value={filters.age_max ?? ""} onChange={setNumber("age_max")} />
            </label>
            <label className="filters-field">
              Min fame rating
              <Input type="number" min={0} max={10} value={filters.fame_min ?? ""} onChange={setNumber("fame_min")} />
            </label>
            <label className="filters-field">
              Max fame rating
              <Input type="number" min={0} max={10} value={filters.fame_max ?? ""} onChange={setNumber("fame_max")} />
            </label>
            <label className="filters-field">
              Max distance (km)
              <Input type="number" min={0} value={filters.distance_max ?? ""} onChange={setNumber("distance_max")} />
            </label>

            {variant === "browse" && (
              <label className="filters-field">
                Min common tags
                <Input type="number" min={0} value={filters.min_common_tags ?? ""} onChange={setNumber("min_common_tags")} />
              </label>
            )}

            {variant === "search" && (
              <>
                <label className="filters-field">
                  City
                  <Input type="text" placeholder="Paris" value={filters.city ?? ""} onChange={setText("city")} />
                </label>
                <label className="filters-field">
                  Tags (comma separated)
                  <Input type="text" placeholder="#geek,#vegan" value={filters.tags ?? ""} onChange={setText("tags")} />
                </label>
              </>
            )}

            <label className="filters-field">
              Sort by
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
              Order
              <Select
                value={filters.order ?? ""}
                onChange={(e) => onChange({ ...filters, order: (e.target.value || undefined) as SortOrder | undefined })}
              >
                <option value="">Auto</option>
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </Select>
            </label>
          </div>

          <Button type="submit">
            {variant === "search" ? "Search" : "Apply"}
          </Button>
        </form>
      )}
    </div>
  )
}
