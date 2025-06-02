export function getImageSrc(image_url?: string): string {
  return image_url && image_url.trim() !== ''
    ? `http://localhost:8001/media/${image_url}`
    : '/images/default.png';
}