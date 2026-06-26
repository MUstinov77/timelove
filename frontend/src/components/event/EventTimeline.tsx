import { EventTimelineItem } from '@/components/event/EventTimelineItem'
import type { TimelineEventView } from '@/types/views'

interface EventTimelineProps {
  timelineId: number
  events: TimelineEventView[]
}

export function EventTimeline({ timelineId, events }: EventTimelineProps) {
  return (
    <div className="event-timeline">
      {events.map((event, index) => (
        <EventTimelineItem
          key={event.id}
          timelineId={timelineId}
          event={event}
          isLast={index === events.length - 1}
        />
      ))}
    </div>
  )
}
