import { useEffect, useState } from "react";

export const useEntryCount = () => {
  const [entryCount, setEntryCount] = useState<{ anime: number; manga: number; scan: number; episode_anime: number; tome_manga: number; tome_scan: number }>({
    anime: 0,
    manga: 0,
    scan: 0,
    episode_anime: 0,
    tome_manga: 0,
    tome_scan: 0,
  });

  useEffect(() => {
    fetch("http://localhost:8000/api/entry_count/")
      .then((res) => res.json())
      .then(setEntryCount)
      .catch(console.error);
  }, []);

  return entryCount;
};