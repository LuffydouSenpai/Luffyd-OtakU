export function transformerLabel(label: string): string {
  const mapping: Record<string, string> = {
    episode_anime: "Episodes d'Anime",
    tome_manga: "Tomes Manga",
    tome_scan: "Tomes Scan",
  };

  return mapping[label] || defaultTransformer(label);
}

function defaultTransformer(label: string): string {
  return label
    .split('_')
    .map((word, index) =>
      index === 0
        ? capitalize(plurialize(word))
        : capitalize(word)
    )
    .join(' ');
}

function capitalize(word: string): string {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

function plurialize(word: string): string {
  if (word.endsWith('e')) return word + 's';
  if (word.endsWith('al')) return word.slice(0, -2) + 'aux';
  return word + 's';
}