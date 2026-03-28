import { useState } from "react"
import Select from "../Select"
import Textarea from "../Textarea"
import Input from "../Input"
import Button from "../Button"
import { updateProfile } from "../../services/profile"
import type { Profile, Gender, SexualPreference } from "../../types/profile"
import { BIO_MAX_LENGTH } from "../../constants/profile"
import "./ProfileInfoForm.css"

interface ProfileInfoFormProps {
  profile: Profile
  onUpdate: (profile: Profile) => void
}

export default function ProfileInfoForm({ profile, onUpdate }: ProfileInfoFormProps) {
  const [gender, setGender] = useState<Gender | "">(profile.gender || "")
  const [preference, setPreference] = useState<SexualPreference | "">(profile.sexual_preference || "")
  const [biography, setBiography] = useState(profile.biography || "")
  const [birthDate, setBirthDate] = useState(profile.birth_date || "")
  const [error, setError] = useState("")
  const [saving, setSaving] = useState(false)

  async function handleSave() {
    setError("")
    setSaving(true)
    try {
      const data: Record<string, unknown> = {}
      if (gender) data.gender = gender
      if (preference) data.sexual_preference = preference
      if (biography.trim()) data.biography = biography.trim()
      if (birthDate) data.birth_date = birthDate
      const updated = await updateProfile(data)
      onUpdate(updated)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error saving profile")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ProfileInfoForm">
      <h3>Informations</h3>

      <label>Genre</label>
      <Select value={gender} onChange={(e) => setGender(e.target.value as Gender)}>
        <option value="">-- Choisir --</option>
        <option value="male">Homme</option>
        <option value="female">Femme</option>
        <option value="other">Autre</option>
      </Select>

      <label>Attirance</label>
      <Select value={preference} onChange={(e) => setPreference(e.target.value as SexualPreference)}>
        <option value="">-- Choisir --</option>
        <option value="male">Hommes</option>
        <option value="female">Femmes</option>
        <option value="bisexual">Les deux</option>
      </Select>

      <label>Bio ({biography.length}/{BIO_MAX_LENGTH})</label>
      <Textarea
        value={biography}
        onChange={(e) => setBiography(e.target.value)}
        maxLength={BIO_MAX_LENGTH}
        placeholder="Parle-nous de toi..."
      />

      <label>Date de naissance</label>
      <Input
        type="date"
        value={birthDate}
        onChange={(e) => setBirthDate(e.target.value)}
      />

      {error && <p className="ProfileInfoForm-error">{error}</p>}

      <Button onClick={handleSave} disabled={saving}>
        {saving ? "Sauvegarde..." : "Sauvegarder"}
      </Button>
    </div>
  )
}
