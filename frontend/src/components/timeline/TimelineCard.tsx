import { Link } from 'react-router-dom'
import type { Timeline } from '@/types/timeline'

interface TimelineCardProps {
  timeline: Timeline
}

export function TimelineCard({ timeline }: TimelineCardProps) {
  return (
    <Link to={`/timelines/${timeline.id}`} className="timeline-card">
      <h3>{timeline.title}</h3>
    </Link>
  )
}
