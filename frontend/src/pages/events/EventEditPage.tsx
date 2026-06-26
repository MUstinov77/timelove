import { useNavigate, useParams } from 'react-router-dom'
import { AttachmentGallery } from '@/components/attachment/AttachmentGallery'
import { AttachmentUploader } from '@/components/attachment/AttachmentUploader'
import { EventForm } from '@/components/event/EventForm'
import { PageContainer } from '@/components/layout/AppLayout'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useAttachments } from '@/hooks/useAttachments'
import { useEvent } from '@/hooks/useEvent'
import { useEvents } from '@/hooks/useEvents'
import type { EventCreatePayload } from '@/types/event'

export function EventEditPage() {
  const { timelineId: timelineIdParam, eventId: eventIdParam } = useParams()
  const timelineId = Number(timelineIdParam)
  const eventId = Number(eventIdParam)
  const navigate = useNavigate()
  const { event, loading, error } = useEvent(timelineId, eventId)
  const { updateEvent } = useEvents(timelineId)
  const { attachments, loading: attachmentsLoading, refresh } = useAttachments(
    timelineId,
    eventId,
  )

  const handleSubmit = async (data: EventCreatePayload) => {
    await updateEvent(eventId, data)
    navigate(`/timelines/${timelineId}/events/${eventId}`)
  }

  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!event) return <ErrorMessage message="Событие не найдено" />

  return (
    <PageContainer title="Редактирование события">
      <EventForm
        defaultValues={{
          title: event.title,
          event_date: event.event_date,
          description: event.description,
        }}
        submitLabel="Сохранить"
        onSubmit={handleSubmit}
      />

      <section className="edit-section">
        <h2>Медиафайлы</h2>
        <AttachmentUploader
          timelineId={timelineId}
          eventId={eventId}
          onUploaded={() => void refresh()}
        />
        {attachmentsLoading ? (
          <Spinner />
        ) : (
          <AttachmentGallery attachments={attachments} />
        )}
      </section>
    </PageContainer>
  )
}
