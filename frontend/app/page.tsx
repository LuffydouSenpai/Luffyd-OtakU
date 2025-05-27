'use client';

import { Fragment, useEffect, useState } from 'react';
import Header from '@/components/Header';
import Image from 'next/image';

import SearchBar from '@/components/SearchBar';
import Link from 'next/link';


type Result = {
  id: number;
  main_title: string;
  format: string;
  image_url: string;
  type_support: string;
  year: number;
  slug: string;
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

  const getImageSrc = (image_url?: string) => {
    return image_url && image_url.trim() !== ''
      ? `http://localhost:8001/media/${image_url}`
      : '/images/default.png';
  };

  const animeList = results.filter((item) => item.type_support === "anime");
  const mangaList = results.filter((item) => item.type_support === "manga");
  const scanList = results.filter((item) => item.type_support === "scan");

  // faire une logique pour le nombre de résultats affichés
  const minPerType = 2;

  const selectedAnime = animeList.slice(0, minPerType);
  const selectedManga = mangaList.slice(0, minPerType);
  const selectedScan = scanList.slice(0, minPerType);

  // fusionner les éléments minimaux
  const merged = [...selectedAnime, ...selectedManga, ...selectedScan];

  // Compléter jusqu’à 10 avec le reste, sans doublons
  const alreadyIds = new Set(merged.map((i) => `${i.type_support}-${i.id}`));
  const remaining = results.filter(
    (i) => !alreadyIds.has(`${i.type_support}-${i.id}`)
  );

  const finalResults = [...merged, ...remaining.slice(0, 10 - merged.length)];


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
            {["anime", "manga", "scan"].map((type) => {
              const filtered = finalResults.filter((item) => item.type_support === type);
              if (filtered.length === 0) return null;

              return (
                <Fragment key={type}>
                  <div className="border-solid border-gray-700 border-1 mb-0 bg-purple-middle">
                    <h2 className="text-xl pl-4 font-bold text-white capitalize">{type}</h2>
                  </div>
                  {filtered.map((item) => (
                    <Link key={`${item.type_support}-${item.id}`} href={`/${item.type_support}/${item.slug}`} passHref>
                      <li className="group border-solid border-gray-700 border-1 pl-4 rounded-md mb-0 bg-purple-card shadow-sm hover:bg-purple hover:p-4">
                        <div className="flex">
                          <div className="w-[100px] h-[100px] group-hover:w-auto group-hover:h-auto flex justify-center items-center overflow-hidden">
                            <Image
                              src={getImageSrc(item.image_url)}
                              alt={`image de ${item.type_support}`}
                              width={100}
                              height={100}
                              className="rounded-xl mx-auto shadow-md object-contain"
                              unoptimized
                            />
                          </div>
                          <div className="ml-4 flex flex-col justify-center">
                            <p className="font-bold text-white">{item.main_title}</p>
                            <span className="text-xs text-perso-gray">
                              ({item.format}, {item.year})
                            </span>
                          </div>
                        </div>
                      </li>
                    </Link>
                  ))}
                </Fragment>
              );
            })}
          </ul>
        </div>
        {/* Ajoute ici tes composants ou sections futures */}
      </main >
    </>
  );
}
