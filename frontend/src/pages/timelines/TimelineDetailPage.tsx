import { EventTimeline } from '@/components/event/EventTimeline'
import { TimelineHeader } from '@/components/timeline/TimelineHeader'
import { EmptyState } from '@/components/ui/EmptyState'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useEvents } from '@/hooks/useEvents'
import { usePermissions } from '@/hooks/usePermissions'
import { useTimelineContext } from '@/hooks/useTimelineContext'

export function TimelineDetailPage() {
  const { timeline } = useTimelineContext()
  const { events, loading: eventsLoading, error: eventsError } = useEvents(timeline.id)
  const { canCreateEvent } = usePermissions(timeline.member_permission)

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

      <EventTimeline timelineId={timeline.id} events={events} />
    </div>
  )
}
