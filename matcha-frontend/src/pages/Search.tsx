import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { ProfileStack } from "../components/ProfileCard"
import type { ProfileCardData } from "../components/ProfileCard"
import ProfileFilters from "../components/ProfileFilters"
import Topbar from "../components/Topbar"
import StatusMessage from "../components/StatusMessage"
import { useAuth } from "../context/AuthContext"
import { searchProfiles } from "../services/browse"
import { likeUser } from "../services/social"
import { toCardData } from "../utils/profileCard"
import type { BrowseFilters } from "../types/browse"

/* Recherche avancée : tranche d'âge, popularité, localisation, tags — mêmes cards que le feed */
export default function Search() {
    const { isAuthenticated } = useAuth()
    const navigate = useNavigate()
    const [filters, setFilters] = useState<BrowseFilters>({ sort_by: "score" })
    const [profiles, setProfiles] = useState<ProfileCardData[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const runSearch = useCallback(async (activeFilters: BrowseFilters) => {
        setLoading(true)
        setError(null)
        try {
            const results = await searchProfiles(activeFilters)
            setProfiles(results.map(toCardData))
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if (!isAuthenticated) return
        runSearch(filters)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isAuthenticated, runSearch])

    if (!isAuthenticated) {
        return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
    }

    const handleLike = async (userId: number) => {
        setError(null)
        try {
            await likeUser(userId)
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        }
    }

    return (
        <div className="app-container page-scroll">
        <Topbar></Topbar>
        <div className="feed-content">
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>}
            <h1>Recherche</h1>
            <ProfileFilters
                variant="search"
                filters={filters}
                onChange={setFilters}
                onApply={() => runSearch(filters)}
            />
            {loading ? (
                <p>Chargement...</p>
            ) : (
                <>
                    <p className="search-count">{profiles.length} profil(s) trouvé(s)</p>
                    <ProfileStack
                        profiles={profiles}
                        onLike={handleLike}
                        onDislike={() => setError(null)}
                        onOpenProfile={(userId) => navigate(`/user/${userId}`)}
                    />
                </>
            )}
        </div>
        </div>
    );
}
