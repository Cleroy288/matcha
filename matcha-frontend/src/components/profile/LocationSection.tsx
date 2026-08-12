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

/* Location (subject IV.2) under explicit GDPR consent: the GPS is never
   queried until the box is checked, and unchecking it clears the coordinates.
   Without GPS, the manually typed city acts as the approximate position. */
export default function LocationSection({ latitude, longitude, city, gpsConsent, onUpdate }: LocationSectionProps) {
  const [lat, setLat] = useState(latitude)
  const [lng, setLng] = useState(longitude)
  const [cityValue, setCityValue] = useState(city || "")
  const [consent, setConsent] = useState(gpsConsent)
  const [error, setError] = useState("")
  const [saving, setSaving] = useState(false)
  const [locating, setLocating] = useState(false)

  /* Consent withdrawal: the coordinates are cleared from the UI right away,
     and the next save resets them to NULL in the database. */
  function handleConsentChange(granted: boolean) {
    setConsent(granted)
    setError("")
    if (!granted) {
      setLat(null)
      setLng(null)
    }
  }

  function handleGPS() {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser")
      return
    }

    setLocating(true)
    setError("")
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLat(position.coords.latitude)
        setLng(position.coords.longitude)
        setLocating(false)
      },
      () => {
        setError("Could not get your position")
        setLocating(false)
      }
    )
  }

  async function handleSave() {
    const trimmedCity = cityValue.trim()
    const validationError = validateLocation(consent, lat, lng, trimmedCity)
    if (validationError) {
      setError(validationError)
      return
    }

    const nextLat = consent ? lat : null
    const nextLng = consent ? lng : null

    setError("")
    setSaving(true)
    try {
      await updateLocation({
        latitude: nextLat,
        longitude: nextLng,
        city: trimmedCity,
        gps_consent: consent
      })
      onUpdate(nextLat, nextLng, trimmedCity, consent)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error saving location")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="LocationSection">
      <h3>Location</h3>

      <p className="LocationSection-notice">
        Your location is used only to suggest and sort profiles near you, and to
        show a distance on your profile. Your exact coordinates are never shown
        to other users. Consent is optional and you can withdraw it at any time:
        unchecking the box deletes the stored coordinates.
      </p>

      <label className="LocationSection-consent">
        <input
          type="checkbox"
          checked={consent}
          onChange={(e) => handleConsentChange(e.target.checked)}
        />
        I consent to sharing my GPS position
      </label>

      {consent && (
        <>
          <Button onClick={handleGPS} disabled={locating}>
            {locating ? "Locating..." : "Use my GPS"}
          </Button>

          {lat !== null && lng !== null && (
            <p className="LocationSection-coords">
              {lat.toFixed(COORDINATE_DECIMALS)}, {lng.toFixed(COORDINATE_DECIMALS)}
            </p>
          )}
        </>
      )}

      <label>{consent ? "City (optional)" : "City or district"}</label>
      <Input
        value={cityValue}
        onChange={(e) => setCityValue(e.target.value)}
        placeholder="Paris, Lyon..."
      />

      {error && <p className="LocationSection-error">{error}</p>}

      <Button onClick={handleSave} disabled={saving}>
        {saving ? "Saving..." : "Save"}
      </Button>
    </div>
  )
}

/* Without consent the city becomes mandatory: the subject requires an
   approximate position for matching. Returns an error message, or "" if valid. */
function validateLocation(
  consent: boolean,
  lat: number | null,
  lng: number | null,
  city: string
): string {
  if (!consent && !city) {
    return "City or district is required when GPS is not allowed"
  }
  if (consent && (lat === null || lng === null)) {
    return "Position is required, or uncheck GPS consent and fill in your city"
  }
  return ""
}
