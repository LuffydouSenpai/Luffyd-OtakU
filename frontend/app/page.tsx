'use client';

import { Fragment, useEffect, useState, useRef } from 'react';
import Header from '@/components/Header';
import Image from 'next/image';

import SearchBar from '@/components/SearchBar';
import Link from 'next/link';
import Footer from '@/components/Footer';
import { transformerLabel } from '../lib/labelTransformer';
import { useSearch } from '../hooks/useSearch';
import { useEntryCount } from '../hooks/useEntryCount';
import { distributeResults } from '../utils/distributeResults';
import { getImageSrc } from '../utils/image';
import { numberToGifArray } from '../utils/numberToGifArray';


export default function Home() {
  const [query, setQuery] = useState('');
  const [showResults, setShowResults] = useState(false);
  const searchBarRef = useRef<HTMLDivElement>(null);
  const { results, loading } = useSearch(query);
  const entryCount = useEntryCount();
  const finalResults = distributeResults(results);
  
  type TypeSupport = "anime" | "manga" | "scan";
  const types: TypeSupport[] = ["anime", "manga", "scan"];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchBarRef.current && !searchBarRef.current.contains(event.target as Node)) {
        setShowResults(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    setShowResults(!!query.trim());
  }, [query]);


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
          <div className="max-w-4xl mx-auto px-6 py-10 relative" >
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
              <ul className="absolute left-0 w-full z-50 rounded-md shadow-lg mt-1">
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
                          <li className="group border-solid border-gray-700 border-1 pl-4 rounded-md mb-0 bg-purple-card shadow-sm hover:bg-purple hover:py-2">
                            <div className="flex">
                              <div className="w-[80px] h-[60px] group-hover:w-auto group-hover:h-auto flex justify-center items-center overflow-hidden">
                                <Image
                                  src={getImageSrc(item.image_url)}
                                  alt={`image de ${item.type_support}`}
                                  width={80}
                                  height={60}
                                  className="rounded-xl mx-auto shadow-md object-contain"
                                  unoptimized
                                />
                              </div>
                              <div className="ml-4 flex flex-col justify-center">
                                <p className="font-bold text-white">{item.main_title}</p>
                                <span className="text-xs text-perso-gray">
                                  {item.type_support === "anime"
                                    ? `(${item.format}, ${item.year})`
                                    : `(${item.type_support}, ${item.year})`}
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
        <section>
          <div className='flex gap-24 p-4 mt-20'>
            {["episode_anime", "tome_manga", "tome_scan"].map((entryKey) => {
              const value = entryCount[entryKey as keyof typeof entryCount];

              return (
                <div key={entryKey} className="border bg-purple-card flex-1 mx-2 text-center py-6">
                  <p className="text-3xl text-white p-8 capitalize"> {transformerLabel(entryKey)}</p>
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
