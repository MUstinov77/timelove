import type { Event } from '@/types/event'

export function sortEventsByDate<T extends Event>(events: T[]): T[] {
  return [...events].sort(
    (a, b) => new Date(b.event_date).getTime() - new Date(a.event_date).getTime(),
  )
}
