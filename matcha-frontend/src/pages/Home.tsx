import { useState, useEffect } from "react";
import { ProfileStack } from "../components/ProfileCard";
import type { ProfileCardData } from "../components/ProfileCard";
import { API_ROUTES } from "../config/api";
import  { likeUser } from "../services/social"
import Topbar from "../components/Topbar"
import { useAuth } from "../context/AuthContext"
import StatusMessage from "../components/StatusMessage"

export default function Feed() {
    const [profiles, setProfiles] = useState<ProfileCardData[]>([]);
    const [error, setError] = useState<string | null>(null)
    // const [success, setSuccess] = useState<string | null>(null)
    
    // exemple: à modifer avec l'algo de suggestion
    useEffect(() => {
        const fetchProfiles = async () => {
            const results: ProfileCardData[] = [];

            const ids = Array.from({ length: 10 }, (_, i) => i + 1);

            await Promise.allSettled(
                ids.map(async (id) => {
          try {
            const res = await fetch(`${API_ROUTES.profile}/${id}`, {
                method: "GET",
              credentials: "include",
            });
            if (!res.ok) return;
            console.log("ok")
            const u = await res.json();

            const age = u.birth_date
              ? Math.floor(
                  (Date.now() - new Date(u.birth_date).getTime()) /
                    (1000 * 60 * 60 * 24 * 365.25)
                )
              : null;

            if (!age) return; // profil incomplet, on skip

            results.push({
              userId: id,
              name: u.first_name ?? `User ${id}`,
              age,
              distance: u.distance_km ? Math.round(u.distance_km) : 0,
              photoUrl: u.profile_photo_url ?? undefined,
            });
          } catch {
            // skip
          }
        })
      );

      results.sort((a, b) => a.userId - b.userId);
      setProfiles(results);
    };
    
    fetchProfiles();
}, []);

    const { isAuthenticated } = useAuth()

    if (!isAuthenticated) {
        return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
    }

    const handleLike = async (userId: number) => {
        setError(null);
        try { 
            await likeUser(userId); 
        } catch {
                setError("Personne déjà like")
        }
    };

    const handleDislike = () => {setError(null);};


    return (
        <div className="app-container">
        <Topbar></Topbar>
        <div className="feed-content">
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)}/>} 
            <ProfileStack
                profiles={profiles}
                onLike={handleLike}
                onDislike={handleDislike}
            />
        </div>
        </div>
    );
}