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
  onUpdate: (lat: number | null, lng: number | null, city: string, consent: boolean) => void
}

type LocationMode = "gps" | "manual"

export default function LocationSection({ latitude, longitude, city, gpsConsent, onUpdate }: LocationSectionProps) {
  const [lat, setLat] = useState(latitude)
  const [lng, setLng] = useState(longitude)
  const [cityValue, setCityValue] = useState(city || "")
  const [mode, setMode] = useState<LocationMode>(gpsConsent ? "gps" : "manual")
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
        setMode("gps")
        setLocating(false)
      },
      () => {
        setError("Impossible d'obtenir la position")
        setLocating(false)
      }
    )
  }

  async function handleSave() {
    const city = cityValue.trim()
    if (mode === "manual" && !city) {
      setError("Ville ou quartier requis")
      return
    }
    if (mode === "gps" && (lat === null || lng === null)) {
      setError("Position requise")
      return
    }

    const nextLat = mode === "manual" ? null : lat
    const nextLng = mode === "manual" ? null : lng
    const consent = mode === "gps"

    setError("")
    setSaving(true)
    try {
      await updateLocation({
        latitude: nextLat,
        longitude: nextLng,
        city,
        gps_consent: consent
      })
      onUpdate(nextLat, nextLng, city, consent)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error saving location")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="LocationSection">
      <h3>Localisation</h3>

      <div className="LocationSection-modes" role="group" aria-label="Mode de localisation">
        <button
          type="button"
          className={mode === "gps" ? "is-active" : ""}
          onClick={() => setMode("gps")}
        >
          GPS
        </button>
        <button
          type="button"
          className={mode === "manual" ? "is-active" : ""}
          onClick={() => {
            setMode("manual")
            setLat(null)
            setLng(null)
            setError("")
          }}
        >
          Ville manuelle
        </button>
      </div>

      {mode === "gps" && (
        <>
          <Button onClick={handleGPS} disabled={locating}>
            {locating ? "Localisation..." : "Utiliser le GPS"}
          </Button>

          {lat !== null && lng !== null && (
            <p className="LocationSection-coords">
              {lat.toFixed(COORDINATE_DECIMALS)}, {lng.toFixed(COORDINATE_DECIMALS)}
            </p>
          )}
        </>
      )}

      <label>{mode === "manual" ? "Ville ou quartier" : "Ville (optionnelle)"}</label>
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
