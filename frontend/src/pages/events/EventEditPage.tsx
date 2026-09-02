import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { AttachmentGallery } from '@/components/attachment/AttachmentGallery'
import { AttachmentUploader } from '@/components/attachment/AttachmentUploader'
import { EventForm } from '@/components/event/EventForm'
import { PageContainer } from '@/components/layout/AppLayout'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useAttachments } from '@/hooks/useAttachments'
import { useEvent } from '@/hooks/useEvent'
import { useEvents } from '@/hooks/useEvents'
import { usePermissions } from '@/hooks/usePermissions'
import { useTimelineContext } from '@/hooks/useTimelineContext'
import type { EventCreatePayload } from '@/types/event'

export function EventEditPage() {
  const { timeline } = useTimelineContext()
  const { eventId: eventIdParam } = useParams()
  const eventId = Number(eventIdParam)
  const navigate = useNavigate()
  const { canEditEvent } = usePermissions(timeline.member_permission)
  const { event, loading, error } = useEvent(timeline.id, eventId)
  const { updateEvent } = useEvents(timeline.id)
  const { attachments, loading: attachmentsLoading, refresh } = useAttachments(
    timeline.id,
    eventId,
  )

  const handleSubmit = async (data: EventCreatePayload) => {
    await updateEvent(eventId, data)
    navigate(`/timelines/${timeline.id}/events/${eventId}`)
  }

  if (!canEditEvent) {
    return <Navigate to={`/timelines/${timeline.id}/events/${eventId}`} replace />
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
          timelineId={timeline.id}
          eventId={eventId}
          onUploaded={() => void refresh()}
        />
        {attachmentsLoading ? (
          <Spinner />
        ) : (
          <AttachmentGallery
            timelineId={timeline.id}
            eventId={eventId}
            attachments={attachments}
          />
        )}
      </section>
    </PageContainer>
  )
}
