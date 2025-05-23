export const runtime = 'nodejs';

import Header from '@/components/Header';
import { notFound } from 'next/navigation';

type Params = { slug: string };

export default async function AnimePage({ params }: { params: Params }) {
  console.log(params.slug);

  const res = await fetch(`http://backend:8000/api/animes/?slug=${params.slug}`, {
    cache: 'no-store',
  });

  if (!res.ok) return notFound();

  const data = await res.json();
  const anime = data[0];
  if (!anime) return notFound();

  return (
    <>
      <Header />
      <main className="max-w-4xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-4">{anime.main_title}</h1>
        <p className="text-gray-700 mb-6">{anime.synopsis}</p>

        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2">Autres titres</h2>
          <ul className="list-disc list-inside text-sm text-gray-600">
            {anime.titles.map((t, i) => (
              <li key={i}>
                {t.title} {t.is_main && <strong className="text-pink-600">(principal)</strong>}
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-2">Images</h2>
          <div className="grid grid-cols-2 gap-4">
            {anime.images.map((img, i) => (
              <div key={i} className="rounded overflow-hidden border">
                <img src={img.image} alt={img.description} className="w-full h-auto" />
                <p className="text-sm text-center text-gray-500 p-1">{img.description}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}