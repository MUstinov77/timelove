import { formatEventDateShort } from '@/utils/formatDate'

interface EventDateBadgeProps {
  date: string
}

export function EventDateBadge({ date }: EventDateBadgeProps) {
  return <time className="event-date-badge">{formatEventDateShort(date)}</time>
}
