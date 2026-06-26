import { useNavigate, useParams } from 'react-router-dom'
import { PageContainer } from '@/components/layout/AppLayout'
import { EventForm } from '@/components/event/EventForm'
import { useEvents } from '@/hooks/useEvents'
import type { EventCreatePayload } from '@/types/event'

export function EventCreatePage() {
  const { timelineId: timelineIdParam } = useParams()
  const timelineId = Number(timelineIdParam)
  const navigate = useNavigate()
  const { createEvent } = useEvents(timelineId)

  const handleSubmit = async (data: EventCreatePayload) => {
    const event = await createEvent(data)
    navigate(`/timelines/${timelineId}/events/${event.id}`)
  }

  return (
    <PageContainer title="Новое событие">
      <EventForm submitLabel="Создать" onSubmit={handleSubmit} />
    </PageContainer>
  )
}
