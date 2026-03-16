import { useState } from "react"
import Input from "../Input"
import Button from "../Button"
import { updateLocation } from "../../services/profile"
import { COORDINATE_DECIMALS } from "../../constants/profile"
import "./LocationSection.css"

interface LocationSectionProps {
  latitude: number | null
  longitude: number | null
  city: string | null
  gpsConsent: boolean
  onUpdate: (lat: number, lng: number, city: string, consent: boolean) => void
}

export default function LocationSection({ latitude, longitude, city, gpsConsent, onUpdate }: LocationSectionProps) {
  const [lat, setLat] = useState(latitude)
  const [lng, setLng] = useState(longitude)
  const [cityValue, setCityValue] = useState(city || "")
  const [consent, setConsent] = useState(gpsConsent)
  const [error, setError] = useState("")
  const [saving, setSaving] = useState(false)
  const [locating, setLocating] = useState(false)

  function handleGPS() {
    if (!navigator.geolocation) {
      setError("Geolocation non supportee par ce navigateur")
      return
    }

    setLocating(true)
    setError("")
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLat(position.coords.latitude)
        setLng(position.coords.longitude)
        setConsent(true)
        setLocating(false)
      },
      () => {
        setError("Impossible d'obtenir la position")
        setLocating(false)
      }
    )
  }

  async function handleSave() {
    if (lat === null || lng === null) {
      setError("Position requise")
      return
    }

    setError("")
    setSaving(true)
    try {
      await updateLocation({
        latitude: lat,
        longitude: lng,
        city: cityValue.trim(),
        gps_consent: consent
      })
      onUpdate(lat, lng, cityValue.trim(), consent)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error saving location")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="LocationSection">
      <h3>Localisation</h3>

      <Button onClick={handleGPS} disabled={locating}>
        {locating ? "Localisation..." : "Utiliser le GPS"}
      </Button>

      {lat !== null && lng !== null && (
        <p className="LocationSection-coords">
          {lat.toFixed(COORDINATE_DECIMALS)}, {lng.toFixed(COORDINATE_DECIMALS)}
        </p>
      )}

      <label>Ville</label>
      <Input
        value={cityValue}
        onChange={(e) => setCityValue(e.target.value)}
        placeholder="Paris, Lyon..."
      />

      {error && <p className="LocationSection-error">{error}</p>}

      <Button onClick={handleSave} disabled={saving}>
        {saving ? "Sauvegarde..." : "Sauvegarder"}
      </Button>
    </div>
  )
}
