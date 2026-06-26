import { Link } from 'react-router-dom'
import { formatEventDateShort } from '@/utils/formatDate'
import type { Event } from '@/types/event'

interface EventCardProps {
  timelineId: number
  event: Event
}

export function EventCard({ timelineId, event }: EventCardProps) {
  return (
    <Link to={`/timelines/${timelineId}/events/${event.id}`} className="event-card">
      <time className="event-card-date">{formatEventDateShort(event.event_date)}</time>
      <h3>{event.title}</h3>
      {event.description && <p>{event.description}</p>}
    </Link>
  )
}
