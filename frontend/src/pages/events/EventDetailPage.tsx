import { Link, useParams } from 'react-router-dom'
import { AttachmentGallery } from '@/components/attachment/AttachmentGallery'
import { PageContainer } from '@/components/layout/AppLayout'
import { Button } from '@/components/ui/Button'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useAttachments } from '@/hooks/useAttachments'
import { useEvent } from '@/hooks/useEvent'
import { usePermissions } from '@/hooks/usePermissions'
import { formatEventDate } from '@/utils/formatDate'

export function EventDetailPage() {
  const { timelineId: timelineIdParam, eventId: eventIdParam } = useParams()
  const timelineId = Number(timelineIdParam)
  const eventId = Number(eventIdParam)
  const { event, loading, error } = useEvent(timelineId, eventId)
  const { attachments, loading: attachmentsLoading } = useAttachments(timelineId, eventId)
  const { canEditEvent } = usePermissions()

  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!event) return <ErrorMessage message="Событие не найдено" />

  return (
    <PageContainer
      title={event.title}
      actions={
        canEditEvent && (
          <Link to={`/timelines/${timelineId}/events/${eventId}/edit`}>
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
        <AttachmentGallery attachments={attachments} />
      )}
    </PageContainer>
  )
}
