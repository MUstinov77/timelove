import { useNavigate } from 'react-router-dom'
import { EventDateBadge } from '@/components/event/EventDateBadge'
import type { TimelineEventView } from '@/types/views'

interface EventTimelineItemProps {
  timelineId: number
  event: TimelineEventView
  isLast: boolean
}

export function EventTimelineItem({ timelineId, event, isLast }: EventTimelineItemProps) {
  const navigate = useNavigate()

  return (
    <div className={`timeline-item ${isLast ? 'timeline-item--last' : ''}`}>
      <div className="timeline-marker" />
      <div
        className="timeline-content"
        onClick={() => navigate(`/timelines/${timelineId}/events/${event.id}`)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter') navigate(`/timelines/${timelineId}/events/${event.id}`)
        }}
      >
        <EventDateBadge date={event.event_date} />
        <h3>{event.title}</h3>
        {event.description && <p className="timeline-description">{event.description}</p>}
      </div>
    </div>
  )
}
