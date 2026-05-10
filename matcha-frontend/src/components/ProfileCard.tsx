import { useRef, useState } from "react";
import "./ProfileCard.css";

export interface ProfileCardData {
  userId: number;
  name: string;
  age: number;
  distance: number;
  photoUrl?: string;
}

interface ProfileCardProps {
  profile: ProfileCardData;
  onLike: (userId: number) => void;
  onDislike: (userId: number) => void;
  /** Stack index: 0 = front, 1 = mid, 2 = back */
  stackIndex?: 0 | 1 | 2;
}

export function ProfileCard({profile, onLike, onDislike, stackIndex = 0,}: ProfileCardProps) {
    const cardRef = useRef<HTMLDivElement>(null);
    const [hint, setHint] = useState<"like" | "nope" | null>(null);
    const dragState = useRef({ active: false, startX: 0, currentX: 0 });

    const applyDrag = (dx: number) => {
        const card = cardRef.current;
        if (!card) return;
        const rot = dx * 0.08;
        card.style.transform = `rotate(${rot}deg) translate(${dx}px, ${
        Math.abs(dx) * 0.04
        }px)`;
        if (dx > 20) setHint("like");
        else if (dx < -20) setHint("nope");
        else setHint(null);
    };

    const settle = (dx: number) => {
        dragState.current.active = false;
        if (dx > 80) {
        flyOut("right");
        } else if (dx < -80) {
        flyOut("left");
        } else {
        const card = cardRef.current;
        if (card) {
            card.style.transition = "transform 0.3s";
            card.style.transform = "";
        }
        setHint(null);
        }
        dragState.current.currentX = 0;
    };

    const flyOut = (dir: "left" | "right") => {
        const card = cardRef.current;
        if (!card) return;
        const tx = dir === "right" ? 700 : -700;
        const rot = dir === "right" ? 25 : -25;
        card.style.transition = "transform 0.35s ease, opacity 0.35s";
        card.style.transform = `rotate(${rot}deg) translate(${tx}px, 80px)`;
        card.style.opacity = "0";
        setHint(null);
        setTimeout(() => {
        if (dir === "right") onLike(profile.userId);
        else onDislike(profile.userId);
        }, 370);
    };

    // Mouse
    const onMouseDown = (e: React.MouseEvent) => {
        if (stackIndex !== 0) return;
        dragState.current = { active: true, startX: e.clientX, currentX: 0 };
        const card = cardRef.current;
        if (card) card.style.transition = "none";
    };
    const onMouseMove = (e: React.MouseEvent) => {
        if (!dragState.current.active) return;
        const dx = e.clientX - dragState.current.startX;
        dragState.current.currentX = dx;
        applyDrag(dx);
    };
    const onMouseUp = () => {
        if (!dragState.current.active) return;
        settle(dragState.current.currentX);
    };

    // Touch
    const onTouchStart = (e: React.TouchEvent) => {
        if (stackIndex !== 0) return;
        dragState.current = {
        active: true,
        startX: e.touches[0].clientX,
        currentX: 0,
        };
        const card = cardRef.current;
        if (card) card.style.transition = "none";
    };
    const onTouchMove = (e: React.TouchEvent) => {
        if (!dragState.current.active) return;
        const dx = e.touches[0].clientX - dragState.current.startX;
        dragState.current.currentX = dx;
        applyDrag(dx);
    };
    const onTouchEnd = () => {
        if (!dragState.current.active) return;
        settle(dragState.current.currentX);
    };

    const stackClass =
        stackIndex === 0 ? "pc-front" : stackIndex === 1 ? "pc-back1" : "pc-back2";

    return (
        <div
        ref={cardRef}
        className={`pc-card ${stackClass}`}
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}
        onMouseLeave={onMouseUp}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
        >
        {/* Photo */}
        {profile.photoUrl ? (
            <img
            className="pc-photo"
            src={profile.photoUrl}
            alt={profile.name}
            draggable={false}
            />
        ) : (
            <div className="pc-photo-placeholder" aria-hidden="true">
            <span>👤</span>
            </div>
        )}

        {/* Swipe hints */}
        <span
            className="pc-hint pc-hint-like"
            style={{ opacity: hint === "like" ? 1 : 0 }}
            aria-hidden="true"
        >
            LIKE
        </span>
        <span
            className="pc-hint pc-hint-nope"
            style={{ opacity: hint === "nope" ? 1 : 0 }}
            aria-hidden="true"
        >
            NOPE
        </span>

        {/* Info overlay */}
        <div className="pc-overlay">
            <p className="pc-name">{profile.name}</p>
            <div className="pc-meta">
            <span className="pc-age">{profile.age} ans</span>
            <span className="pc-dist">{profile.distance} km</span>
            </div>
        </div>
        </div>
    );
}

/* ─── Action buttons (séparés pour réutilisation) ─── */

interface ProfileCardActionsProps {
  userId: number;
  onLike: (id: number) => void;
  onDislike: (id: number) => void;
}

export function ProfileCardActions({
  userId,
  onLike,
  onDislike,
}: ProfileCardActionsProps) {
  return (
    <div className="pc-actions">
      <div className="pc-action-wrap">
        <button
          className="pc-btn pc-btn-dislike"
          onClick={() => onDislike(userId)}
          aria-label="Dislike"
        >
          ✕
        </button>
        <span className="pc-btn-label">Nope</span>
      </div>
      <div className="pc-action-wrap">
        <button
          className="pc-btn pc-btn-like"
          onClick={() => onLike(userId)}
          aria-label="Like"
        >
          ♥
        </button>
        <span className="pc-btn-label">Like</span>
      </div>
    </div>
  );
}

/* ─── Stack wrapper (Feed / Recherche) ─── */

interface ProfileStackProps {
  profiles: ProfileCardData[];
  onLike: (userId: number) => void;
  onDislike: (userId: number) => void;
}

export function ProfileStack({
  profiles,
  onLike,
  onDislike,
}: ProfileStackProps) {
  const [index, setIndex] = useState(0);

  const handleLike = (userId: number) => {
    onLike(userId);
    setIndex((i) => i + 1);
  };
  const handleDislike = (userId: number) => {
    onDislike(userId);
    setIndex((i) => i + 1);
  };

  const current = profiles[index];

  if (index >= profiles.length) {
    return (
      <div className="pc-empty">
        <p className="pc-empty-text">Personne ...</p>
      </div>
    );
  }

  return (
    <div className="pc-stack-wrapper">
    <div className="pc-stack">
      {/* Cards décoratives vides — jamais de contenu visible */}
      <div className="pc-card pc-back2" />
      <div className="pc-card pc-back1" />

      {/* Seulement la card front avec le vrai profil */}
      <ProfileCard
        key={profiles[index].userId}
        profile={profiles[index]}
        stackIndex={0}
        onLike={handleLike}
        onDislike={handleDislike}
      />
    </div>
    <ProfileCardActions
      userId={current.userId}
      onLike={handleLike}
      onDislike={handleDislike}
    />
  </div>
  );
}