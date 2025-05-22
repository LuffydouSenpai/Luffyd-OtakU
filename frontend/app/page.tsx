'use client';


import Head from 'next/head';
import Header from '@/components/Header';
import Image from 'next/image';

import SearchBar from '@/components/SearchBar';

export default function Home() {

  const handleSearch = (query: string) => {
    console.log('Recherche :', query);
    // Intègre ici navigation, filtre ou requête API
  };

  return (
    <>
      <Head>
        <title>Luffyd'OtakU - Accueil</title>
        <meta name="description" content="Gestionnaire personnel de mangas et animes" />
      </Head>

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
          <SearchBar onSearch={handleSearch} />
        </div>
        {/* Ajoute ici tes composants ou sections futures */}
      </main>
    </>
  );
}
