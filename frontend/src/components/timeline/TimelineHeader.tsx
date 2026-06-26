import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/Button'
import type { Timeline } from '@/types/timeline'

interface TimelineHeaderProps {
  timeline: Timeline
  canCreateEvent?: boolean
}

export function TimelineHeader({ timeline, canCreateEvent }: TimelineHeaderProps) {
  return (
    <div className="timeline-header">
      <div>
        <h1>{timeline.title}</h1>
      </div>
      {canCreateEvent && (
        <Link to={`/timelines/${timeline.id}/events/new`}>
          <Button>+ Событие</Button>
        </Link>
      )}
    </div>
  )
}
