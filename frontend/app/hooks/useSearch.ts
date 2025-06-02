import { useEffect, useState } from "react";

export type Result = {
  id: number;
  main_title: string;
  format: string;
  image_url: string;
  type_support: "anime" | "manga" | "scan";
  year: number;
  slug: string;
};

export const useSearch = (query: string) => {
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delay = setTimeout(() => {
      if (query.trim()) {
        setLoading(true);
        fetch(`http://localhost:8000/api/titres/?search=${query}`)
          .then((res) => res.json())
          .then(setResults)
          .catch(console.error)
          .finally(() => setLoading(false));
      } else {
        setResults([]);
      }
    }, 400);

    return () => clearTimeout(delay);
  }, [query]);

  return { results, loading };
};