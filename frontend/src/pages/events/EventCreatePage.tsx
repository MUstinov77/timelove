import { Navigate, useNavigate } from 'react-router-dom'
import { PageContainer } from '@/components/layout/AppLayout'
import { EventForm } from '@/components/event/EventForm'
import { useEvents } from '@/hooks/useEvents'
import { usePermissions } from '@/hooks/usePermissions'
import { useTimelineContext } from '@/hooks/useTimelineContext'
import type { EventCreatePayload } from '@/types/event'

export function EventCreatePage() {
  const { timeline } = useTimelineContext()
  const navigate = useNavigate()
  const { canCreateEvent } = usePermissions(timeline.member_permission)
  const { createEvent } = useEvents(timeline.id)

  const handleSubmit = async (data: EventCreatePayload) => {
    const event = await createEvent(data)
    navigate(`/timelines/${timeline.id}/events/${event.id}`)
  }

  if (!canCreateEvent) {
    return <Navigate to={`/timelines/${timeline.id}`} replace />
  }

  return (
    <PageContainer title="Новое событие">
      <EventForm submitLabel="Создать" onSubmit={handleSubmit} />
    </PageContainer>
  )
}
