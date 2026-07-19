import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { ProfileStack } from "../components/ProfileCard"
import type { ProfileCardData } from "../components/ProfileCard"
import ProfileFilters from "../components/ProfileFilters"
import Topbar from "../components/Topbar"
import StatusMessage from "../components/StatusMessage"
import { useAuth } from "../context/AuthContext"
import { browseProfiles } from "../services/browse"
import { likeUser } from "../services/social"
import { toCardData } from "../utils/profileCard"
import type { BrowseFilters } from "../types/browse"

/* Feed : profils suggérés par l'algo (tags communs + proximité + fame), swipe like/pass */
export default function Home() {
    const { isAuthenticated } = useAuth()
    const navigate = useNavigate()
    const [filters, setFilters] = useState<BrowseFilters>({ sort_by: "score" })
    const [profiles, setProfiles] = useState<ProfileCardData[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    const loadSuggestions = useCallback(async (activeFilters: BrowseFilters) => {
        setLoading(true)
        setError(null)
        try {
            const suggestions = await browseProfiles(activeFilters)
            setProfiles(suggestions.map(toCardData))
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if (!isAuthenticated) return
        loadSuggestions(filters)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isAuthenticated, loadSuggestions])

    if (!isAuthenticated) {
        return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
    }

    const handleLike = async (userId: number) => {
        setError(null)
        try {
            const result = await likeUser(userId)
            if (result.match) {
                setSuccess("C'est un match !")
            }
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        }
    }

    const handleDislike = () => { setError(null) }

    return (
        <div className="app-container page-scroll">
        <Topbar></Topbar>
        <div className="feed-content">
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>}
            {success && <StatusMessage type="success" message={success} onClose={() => setSuccess(null)}/>}
            <ProfileFilters
                variant="browse"
                filters={filters}
                onChange={setFilters}
                onApply={() => loadSuggestions(filters)}
            />
            {loading ? (
                <p>Chargement...</p>
            ) : (
                <ProfileStack
                    profiles={profiles}
                    onLike={handleLike}
                    onDislike={handleDislike}
                    onOpenProfile={(userId) => navigate(`/user/${userId}`)}
                />
            )}
        </div>
        </div>
    );
}
