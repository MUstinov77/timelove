import { Link, useParams } from 'react-router-dom'
import { AttachmentGallery } from '@/components/attachment/AttachmentGallery'
import { PageContainer } from '@/components/layout/AppLayout'
import { Button } from '@/components/ui/Button'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useAttachments } from '@/hooks/useAttachments'
import { useEvent } from '@/hooks/useEvent'
import { usePermissions } from '@/hooks/usePermissions'
import { useTimelineContext } from '@/hooks/useTimelineContext'
import { formatEventDate } from '@/utils/formatDate'

export function EventDetailPage() {
  const { timeline } = useTimelineContext()
  const { eventId: eventIdParam } = useParams()
  const eventId = Number(eventIdParam)
  const { event, loading, error } = useEvent(timeline.id, eventId)
  const { attachments, loading: attachmentsLoading } = useAttachments(timeline.id, eventId)
  const { canEditEvent } = usePermissions(timeline.member_permission)

  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!event) return <ErrorMessage message="Событие не найдено" />

  return (
    <PageContainer
      title={event.title}
      actions={
        canEditEvent && (
          <Link to={`/timelines/${timeline.id}/events/${eventId}/edit`}>
            <Button variant="secondary">Редактировать</Button>
          </Link>
        )
      }
    >
      <time className="event-detail-date">{formatEventDate(event.event_date)}</time>
      <p className="event-detail-description">{event.description}</p>

      {attachmentsLoading ? (
        <Spinner />
      ) : (
        <AttachmentGallery
          timelineId={timeline.id}
          eventId={eventId}
          attachments={attachments}
        />
      )}
    </PageContainer>
  )
}
