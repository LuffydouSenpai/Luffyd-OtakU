// components/Header.tsx

import Link from 'next/link';

export default function Header() {
    return (
        <header className="px-4 bg-purple text-white border-b border-gray-700">
            <div className="container max-w-2/4 mx-auto px-6 py-4 flex flex-col items-center">
                <div>
                    <h1 className="text-4xl pb-4 font-semibold tracking-widest">
                        <Link href="/">Luffyd&apos;OtakU</Link>
                    </h1>
                </div>
                <div className="bg-purple-card p-4 pt-2 pb-2 w-full ">
                    <nav className="flex text-base justify-around items-center w-3/4 mx-auto">
                        <Link href="/anime" className="hover:underline hover:text-pink-500">Anime</Link>
                        <Link href="/manga" className="hover:underline hover:text-pink-500">Manga</Link>
                        <Link href="/scan" className="hover:underline hover:text-pink-500">Scan</Link>
                        <Link href="/library" className="hover:underline hover:text-pink-500">Bibliothèque</Link>
                        <Link href="/statistics" className="hover:underline hover:text-pink-500">Statistiques</Link>
                    </nav>
                </div>
            </div>
        </header>
    );
}
