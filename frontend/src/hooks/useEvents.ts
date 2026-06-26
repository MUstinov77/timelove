import { useCallback, useEffect, useMemo, useState } from 'react'
import { eventService } from '@/services/eventService'
import type { Event, EventCreatePayload, EventUpdatePayload } from '@/types/event'
import type { TimelineEventView } from '@/types/views'
import { sortEventsByDate } from '@/utils/sortEventsByDate'

export function useEvents(timelineId: number) {
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await eventService.getAll(timelineId)
      setEvents(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить события')
    } finally {
      setLoading(false)
    }
  }, [timelineId])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const sortedEvents = useMemo<TimelineEventView[]>(
    () =>
      sortEventsByDate(events).map((event) => ({
        ...event,
        attachmentCount: 0,
      })),
    [events],
  )

  const createEvent = useCallback(
    async (payload: EventCreatePayload) => {
      const event = await eventService.create(timelineId, payload)
      setEvents((prev) => [...prev, event])
      return event
    },
    [timelineId],
  )

  const updateEvent = useCallback(
    async (eventId: number, payload: EventUpdatePayload) => {
      const event = await eventService.update(timelineId, eventId, payload)
      setEvents((prev) => prev.map((e) => (e.id === eventId ? event : e)))
      return event
    },
    [timelineId],
  )

  const deleteEvent = useCallback(
    async (eventId: number) => {
      await eventService.delete(timelineId, eventId)
      setEvents((prev) => prev.filter((e) => e.id !== eventId))
    },
    [timelineId],
  )

  return {
    events: sortedEvents,
    loading,
    error,
    refresh,
    createEvent,
    updateEvent,
    deleteEvent,
  }
}
