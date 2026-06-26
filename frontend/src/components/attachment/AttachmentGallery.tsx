import { AttachmentPreview } from '@/components/attachment/AttachmentPreview'
import type { Attachment } from '@/types/attachment'

interface AttachmentGalleryProps {
  attachments: Attachment[]
}

export function AttachmentGallery({ attachments }: AttachmentGalleryProps) {
  if (attachments.length === 0) return null

  return (
    <div className="attachment-gallery">
      {attachments.map((attachment) => (
        <AttachmentPreview key={attachment.id} attachment={attachment} />
      ))}
    </div>
  )
}
