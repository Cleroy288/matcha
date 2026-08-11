import { useState, useEffect, useRef, type KeyboardEvent } from "react"
import TagChip from "../TagChip"
import Input from "../Input"
import { addTag, removeTag, searchTags } from "../../services/profile"
import type { Tag } from "../../types/profile"
import { MAX_TAGS, MIN_TAGS_FOR_COMPLETE, SEARCH_DEBOUNCE_MS, MIN_SEARCH_LENGTH } from "../../constants/profile"
import "./TagsSection.css"

interface TagsSectionProps {
  tags: Tag[]
  onUpdate: (tags: Tag[]) => void
}

export default function TagsSection({ tags, onUpdate }: TagsSectionProps) {
  const [query, setQuery] = useState("")
  const [suggestions, setSuggestions] = useState<Tag[]>([])
  const [error, setError] = useState("")
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)

    // below the threshold, no search runs (the list is cleared in handleQueryChange)
    if (query.length < MIN_SEARCH_LENGTH) {
      return
    }

    debounceRef.current = setTimeout(async () => {
      try {
        const result = await searchTags(query)
        setSuggestions(result.tags)
      } catch {
        setSuggestions([])
      }
    }, SEARCH_DEBOUNCE_MS)

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [query])

  /* Input: updates the query and clears the suggestions as soon as it is too short */
  function handleQueryChange(value: string) {
    setQuery(value)
    if (value.length < MIN_SEARCH_LENGTH) {
      setSuggestions([])
    }
  }

  async function handleAdd(tagName: string) {
    setError("")
    if (tags.length >= MAX_TAGS) {
      setError(`Maximum ${MAX_TAGS} tags`)
      return
    }
    try {
      const result = await addTag(tagName)
      onUpdate(result.tags)
      setQuery("")
      setSuggestions([])
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error adding tag")
    }
  }

  async function handleRemove(tagName: string) {
    setError("")
    try {
      const result = await removeTag(tagName)
      onUpdate(result.tags)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error removing tag")
    }
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter" && query.trim()) {
      e.preventDefault()
      const tagName = query.startsWith("#") ? query.trim() : `#${query.trim()}`
      handleAdd(tagName)
    }
  }

  return (
    <div className="TagsSection">
      <h3>Tags ({tags.length}/{MAX_TAGS}, minimum {MIN_TAGS_FOR_COMPLETE})</h3>

      <div className="TagsSection-chips">
        {tags.map((tag) => (
          <TagChip key={tag.id} label={tag.name} onRemove={() => handleRemove(tag.name)} />
        ))}
      </div>

      <div className="TagsSection-search">
        <Input
          value={query}
          onChange={(e) => handleQueryChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="#tag (press Enter to add)"
        />
        {suggestions.length > 0 && (
          <div className="TagsSection-dropdown">
            {suggestions.map((s) => (
              <div key={s.id} className="TagsSection-suggestion" onClick={() => handleAdd(s.name)}>
                {s.name}
              </div>
            ))}
          </div>
        )}
      </div>

      {error && <p className="TagsSection-error">{error}</p>}
    </div>
  )
}
