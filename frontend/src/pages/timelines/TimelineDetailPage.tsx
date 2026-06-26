import { useParams } from 'react-router-dom'
import { EventTimeline } from '@/components/event/EventTimeline'
import { TimelineHeader } from '@/components/timeline/TimelineHeader'
import { EmptyState } from '@/components/ui/EmptyState'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useEvents } from '@/hooks/useEvents'
import { usePermissions } from '@/hooks/usePermissions'
import { useTimeline } from '@/hooks/useTimeline'

export function TimelineDetailPage() {
  const { timelineId: timelineIdParam } = useParams()
  const timelineId = Number(timelineIdParam)
  const { timeline, loading: timelineLoading, error: timelineError } = useTimeline(timelineId)
  const { events, loading: eventsLoading, error: eventsError } = useEvents(timelineId)
  const { canCreateEvent } = usePermissions()

  if (timelineLoading) return <Spinner />
  if (timelineError) return <ErrorMessage message={timelineError} />
  if (!timeline) return <ErrorMessage message="Таймлайн не найден" />

  return (
    <div className="page-container">
      <TimelineHeader timeline={timeline} canCreateEvent={canCreateEvent} />

      {eventsLoading && <Spinner />}
      {eventsError && <ErrorMessage message={eventsError} />}

      {!eventsLoading && !eventsError && events.length === 0 && (
        <EmptyState
          title="Пока нет событий"
          description="Добавьте первое событие в этот таймлайн"
        />
      )}

      <EventTimeline timelineId={timelineId} events={events} />
    </div>
  )
}
