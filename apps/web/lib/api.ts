export const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export async function fetchExplosiveScanner() {
  const response = await fetch(`${apiBaseUrl}/api/explosive-scanner`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to load explosive scanner');
  return response.json();
}
