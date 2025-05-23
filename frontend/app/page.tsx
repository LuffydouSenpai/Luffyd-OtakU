'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/Header';
import Image from 'next/image';

import SearchBar from '@/components/SearchBar';


type Result = {
  id: number;
  main_title: string;
  type: string;
};

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delay = setTimeout(() => {
      if (query.trim()) {
        fetch(`http://localhost:8000/api/titres/?search=${query}`)
          .then((res) => res.json())
          .then(setResults)
          .catch(console.error)
          .finally(() => setLoading(false));
      } else {
        setResults([]); // Efface les résultats si champ vide
      }
    }, 400);

    return () => clearTimeout(delay);
  }, [query]);

  return (
    <>
      <Header />

      <main className="max-w-6xl mx-auto px-6 py-10">
        <div className="flex items-center">
          <Image
            src="/images/logo.png"
            alt="Bannière Otaku"
            width={600}
            height={200}
            className="rounded-xl mx-auto shadow-md"
          />
        </div>

        <div className="max-w-4xl mx-auto px-6 py-10">
          <SearchBar value={query} onChange={setQuery} />
          {loading && <p className="mt-4 text-gray-500">Chargement...</p>}

          <ul className="mt-6 space-y-3">
            {results.slice(0, 10).map((item) => (
              <li
                key={`${item.type}-${item.id}`}
                className="border p-4 rounded-md bg-white shadow-sm"
              >
                <p className="font-bold">{item.main_title}</p>
                <span className="text-xs text-gray-500 uppercase">{item.type}</span>
              </li>
            ))}
          </ul>
        </div>
        {/* Ajoute ici tes composants ou sections futures */}
      </main>
    </>
  );
}
