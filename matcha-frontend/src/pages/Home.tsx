import Topbar from "../components/Topbar.tsx"
import { useAuth } from "../context/AuthContext.tsx"

export default function Home() {
  const { user } = useAuth()

  // Mock de données pour visualiser la grille
  const tempProfiles = [
    { id: 1, name: "Alice", age: 24, location: "Paris", tags: ["#art", "#vegan"] },
    { id: 2, name: "Bob", age: 28, location: "Lyon", tags: ["#geek", "#coffee"] },
    { id: 3, name: "Charlie", age: 22, location: "Marseille", tags: ["#sport"] },
  ]

  return (
    <div className="app-container">
      <Topbar />
      <div style={{ paddingTop: "80px" }}>
        <header style={{ marginBottom: "30px" }}>
          <h1>Bienvenue, {user?.username} ! ✨</h1>
          <p>Voici des profils qui pourraient vous plaire :</p>
        </header>

        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", 
          gap: "20px" 
        }}>
          {tempProfiles.map(profile => (
            <div key={profile.id} className="brutal-card" style={{ background: "white" }}>
              <div style={{ 
                width: "100%", 
                height: "200px", 
                background: "#ddd", 
                borderBottom: "3px solid black",
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
              }}>
                [Photo de {profile.name}]
              </div>
              <div style={{ padding: "15px" }}>
                <h3>{profile.name}, {profile.age}</h3>
                <p style={{ fontSize: "0.9rem" }}>📍 {profile.location}</p>
                <div style={{ display: "flex", gap: "5px", flexWrap: "wrap", marginTop: "10px" }}>
                  {profile.tags.map(tag => (
                    <span key={tag} style={{ background: "var(--accent)", padding: "2px 5px", border: "1px solid black", fontSize: "0.8rem" }}>
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}