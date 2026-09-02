import type { JwtPayload } from '@/types/auth'

/** base64url → строка (atob понимает только обычный base64). */
function base64UrlDecode(segment: string): string {
  const base64 = segment.replace(/-/g, '+').replace(/_/g, '/')
  const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), '=')
  const binary = atob(padded)
  // Корректно декодируем UTF-8 (кириллица в username и т.п.).
  const bytes = Uint8Array.from(binary, (ch) => ch.charCodeAt(0))
  return new TextDecoder().decode(bytes)
}

export function decodeJwt(token: string): JwtPayload {
  const payload = token.split('.')[1]
  if (!payload) throw new Error('Invalid token')
  return JSON.parse(base64UrlDecode(payload)) as JwtPayload
}
