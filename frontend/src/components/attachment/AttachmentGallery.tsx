import { AttachmentPreview } from '@/components/attachment/AttachmentPreview'
import type { Attachment } from '@/types/attachment'

interface AttachmentGalleryProps {
  timelineId: number
  eventId: number
  attachments: Attachment[]
}

export function AttachmentGallery({ timelineId, eventId, attachments }: AttachmentGalleryProps) {
  if (attachments.length === 0) return null

  return (
    <div className="attachment-gallery">
      {attachments.map((attachment) => (
        <AttachmentPreview
          key={attachment.id}
          timelineId={timelineId}
          eventId={eventId}
          attachment={attachment}
        />
      ))}
    </div>
  )
}
