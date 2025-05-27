'use client';

import { Fragment, useEffect, useState, useRef } from 'react';
import Header from '@/components/Header';
import Image from 'next/image';

import SearchBar from '@/components/SearchBar';
import Link from 'next/link';
import Footer from '@/components/Footer';


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

  const [showResults, setShowResults] = useState(false);
  const searchBarRef = useRef<HTMLDivElement>(null);

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


  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchBarRef.current && !searchBarRef.current.contains(event.target as Node)) {
        setShowResults(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    if (query.trim()) {
      setShowResults(true);
    } else {
      setShowResults(false);
    }
  }, [query]);

  const getImageSrc = (image_url?: string) => {
    return image_url && image_url.trim() !== ''
      ? `http://localhost:8001/media/${image_url}`
      : '/images/default.png';
  };



  type TypeSupport = "anime" | "manga" | "scan";

  const WEIGHTS: Record<TypeSupport, number> = {
    anime: 5,
    manga: 3,
    scan: 2,
  };

  const MAX_TOTAL = 10;

  // Regroupe les résultats par type
  const finalResults: Record<TypeSupport, Result[]> = {
    anime: [],
    manga: [],
    scan: [],
  };

  for (const item of results) {
    if (item.type_support in finalResults) {
      finalResults[item.type_support as TypeSupport].push(item);
    }
  }

  // Coupe selon le poids
  for (const type of Object.keys(finalResults) as TypeSupport[]) {
    finalResults[type] = finalResults[type].slice(0, WEIGHTS[type]);
  }

  // Calcule total actuel
  const currentTotal = finalResults.anime.length + finalResults.manga.length + finalResults.scan.length;
  let missing = MAX_TOTAL - currentTotal;

  // Si il reste de la place, on réalloue en prenant dans les listes non sélectionnées
  if (missing > 0) {
    // Récupère les extras disponibles en excluant déjà pris
    const extras = [
      ...results.filter(i => i.type_support === "anime").slice(finalResults.anime.length),
      ...results.filter(i => i.type_support === "manga").slice(finalResults.manga.length),
      ...results.filter(i => i.type_support === "scan").slice(finalResults.scan.length),
    ];

    for (const item of extras) {
      if (missing === 0) break;

      const type = item.type_support as TypeSupport;
      finalResults[type].push(item);
      missing--;
    }
  }

  const types: TypeSupport[] = ["anime", "manga", "scan"];

  const [entryCount, setEntryCount] = useState<{ anime: number; manga: number; scan: number }>({
    anime: 0,
    manga: 0,
    scan: 0,
  });

  useEffect(() => {
    fetch('http://localhost:8000/api/entry_count/')
      .then((res) => res.json())
      .then(setEntryCount)
      .catch(console.error);
  }, []);

  const numberToGifArray = (number: number) => {
    return String(number).split('');
  };

  return (
    <>
      <Header />

      <main className="container mx-auto px-6 py-10 flex-grow">

        <section id='banner'>
          <div className="flex items-center">
            <Image
              src="/images/logo.png"
              alt="Bannière Otaku"
              width={600}
              height={200}
              className="rounded-xl mx-auto shadow-md"
            />
          </div>
        </section>

        <section id='searchBar' ref={searchBarRef}>
          <div className="max-w-4xl mx-auto px-6 py-10 relative">
            <SearchBar
              value={query}
              onChange={setQuery}
              onFocus={() => {
                if (query.trim()) setShowResults(true);
              }}
              onClear={() => {
                setQuery('');
                setShowResults(false);
              }} />
            {loading && <p className="mt-4 text-gray-500">Chargement...</p>}

            {showResults && (
              <ul className="absolute w-full">
                {types.map((type) =>
                  finalResults[type].length > 0 && (
                    <Fragment key={type}>
                      <div className="border-solid border-gray-700 border-1 mb-0 bg-purple-middle">
                        <h2 className="text-xl pl-4 font-bold text-white capitalize">{type}</h2>
                      </div>
                      {finalResults[type].map((item) => (
                        <Link
                          key={`${item.type_support}-${item.id}`}
                          href={`/${item.type_support}/${item.slug}`}
                          passHref
                        >
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
                  )
                )}
              </ul>
            )}
          </div>
        </section>

        <section id='entry'>
          <div className='flex gap-24 p-4 mt-20'>
            {["anime", "manga", "scan"].map((entryKey) => {
              const value = entryCount[entryKey as keyof typeof entryCount];

              return (
                <div key={entryKey} className="border bg-purple-card flex-1 mx-2 text-center py-6">
                  <p className="text-3xl text-white p-8 capitalize">Entry {entryKey}</p>
                  <div className="flex justify-center gap-1">
                    {numberToGifArray(value).map((digit, idx) => (
                      <Image
                        key={idx}
                        src={`/entry/${digit}.gif`}
                        alt={`Chiffre ${digit}`}
                        width={50}
                        height={50}
                      />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
        {/* Ajoute ici tes composants ou sections futures */}
      </main >
      <Footer />
    </>
  );
}
