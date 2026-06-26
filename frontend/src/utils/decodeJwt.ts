import type { JwtPayload } from '@/types/auth'

export function decodeJwt(token: string): JwtPayload {
  const payload = token.split('.')[1]
  if (!payload) throw new Error('Invalid token')
  return JSON.parse(atob(payload)) as JwtPayload
}
