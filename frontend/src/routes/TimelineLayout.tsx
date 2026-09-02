import { Navigate, Outlet, useParams } from 'react-router-dom'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useTimeline } from '@/hooks/useTimeline'
import type { TimelineOutletContext } from '@/hooks/useTimelineContext'

/**
 * Layout-маршрут для раздела `/timelines/:timelineId`: один раз грузит
 * таймлайн (вместе с ролью текущего пользователя) и отдаёт его вложенным
 * страницам через outlet-контекст — чтобы деталка и страницы событий не
 * запрашивали таймлайн каждая по отдельности.
 */
export function TimelineLayout() {
  const { timelineId: param } = useParams()
  const timelineId = Number(param)
  const { timeline, loading, error, refresh } = useTimeline(timelineId)

  if (!Number.isInteger(timelineId) || timelineId <= 0) {
    return <Navigate to="/" replace />
  }
  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!timeline) return <ErrorMessage message="Таймлайн не найден" />

  return (
    <Outlet
      context={
        { timeline, refreshTimeline: refresh } satisfies TimelineOutletContext
      }
    />
  )
}
