import { useEffect, useRef } from "react";
import { likeUser, unlikeUser, visitUser } from "../services/social";

interface UseProfileCardOptions {
  userId: number;
  isActive: boolean;
  onLikeSuccess?: (userId: number) => void;
  onDislikeSuccess?: (userId: number) => void;
  onError?: (err: unknown) => void;
}

export function useProfileCard({
  userId,
  isActive,
  onLikeSuccess,
  onDislikeSuccess,
  onError,
}: UseProfileCardOptions) {
  const visitedRef = useRef<number | null>(null);

  useEffect(() => {
    if (!isActive) return;
    if (visitedRef.current === userId) return;
    visitedRef.current = userId;
    visitUser(userId).catch(() => {
    });
  }, [isActive, userId]);

  const handleLike = async () => {
    try {
      await likeUser(userId);
      onLikeSuccess?.(userId);
    } catch (err) {
      onError?.(err);
    }
  };

  const handleDislike = async () => {
    try {
      await unlikeUser(userId);
      onDislikeSuccess?.(userId);
    } catch (err) {
      onError?.(err);
    }
  };

  return { handleLike, handleDislike };
}