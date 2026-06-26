import { useCallback, useEffect, useState } from 'react'
import { timelineService } from '@/services/timelineService'
import type { Timeline, TimelineCreatePayload } from '@/types/timeline'

export function useTimelines() {
  const [timelines, setTimelines] = useState<Timeline[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await timelineService.getAll()
      setTimelines(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить таймлайны')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const createTimeline = useCallback(async (payload: TimelineCreatePayload) => {
    const timeline = await timelineService.create(payload)
    setTimelines((prev) => [...prev, timeline])
    return timeline
  }, [])

  const deleteTimeline = useCallback(async (timelineId: number) => {
    await timelineService.delete(timelineId)
    setTimelines((prev) => prev.filter((t) => t.id !== timelineId))
  }, [])

  return { timelines, loading, error, refresh, createTimeline, deleteTimeline }
}
