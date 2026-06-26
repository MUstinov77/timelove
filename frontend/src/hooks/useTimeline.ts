import { useCallback, useEffect, useState } from 'react'
import { timelineService } from '@/services/timelineService'
import type { Timeline } from '@/types/timeline'

export function useTimeline(timelineId: number) {
  const [timeline, setTimeline] = useState<Timeline | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await timelineService.getById(timelineId)
      setTimeline(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить таймлайн')
    } finally {
      setLoading(false)
    }
  }, [timelineId])

  useEffect(() => {
    void refresh()
  }, [refresh])

  return { timeline, loading, error, refresh }
}
