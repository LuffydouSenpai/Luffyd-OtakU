import { Result } from "../hooks/useSearch";

type TypeSupport = "anime" | "manga" | "scan";

const WEIGHTS: Record<TypeSupport, number> = {
  anime: 5,
  manga: 3,
  scan: 2,
};

const MAX_TOTAL = 10;

export function distributeResults(results: Result[]) {
  const grouped: Record<TypeSupport, Result[]> = {
    anime: [],
    manga: [],
    scan: [],
  };

  for (const item of results) {
    if (item.type_support in grouped) {
      grouped[item.type_support as TypeSupport].push(item);
    }
  }

  for (const type of Object.keys(grouped) as TypeSupport[]) {
    grouped[type] = grouped[type].slice(0, WEIGHTS[type]);
  }

  const currentTotal = grouped.anime.length + grouped.manga.length + grouped.scan.length;
  let missing = MAX_TOTAL - currentTotal;

  if (missing > 0) {
    const extras = [
      ...results.filter(i => i.type_support === "anime").slice(grouped.anime.length),
      ...results.filter(i => i.type_support === "manga").slice(grouped.manga.length),
      ...results.filter(i => i.type_support === "scan").slice(grouped.scan.length),
    ];

    for (const item of extras) {
      if (missing === 0) break;
      grouped[item.type_support as TypeSupport].push(item);
      missing--;
    }
  }

  return grouped;
}