import { useCallback, useEffect, useState } from 'react'
import { eventService } from '@/services/eventService'
import type { Event } from '@/types/event'

export function useEvent(timelineId: number, eventId: number) {
  const [event, setEvent] = useState<Event | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await eventService.getById(timelineId, eventId)
      setEvent(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить событие')
    } finally {
      setLoading(false)
    }
  }, [timelineId, eventId])

  useEffect(() => {
    void refresh()
  }, [refresh])

  return { event, loading, error, refresh }
}
