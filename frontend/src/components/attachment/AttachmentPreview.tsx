import { isImageMime, isVideoMime } from '@/utils/getMediaUrl'
import { ImagePreview } from '@/components/attachment/ImagePreview'
import { VideoPreview } from '@/components/attachment/VideoPreview'
import { Spinner } from '@/components/ui/Spinner'
import { useMediaObjectUrl } from '@/hooks/useMediaObjectUrl'
import type { Attachment } from '@/types/attachment'

interface AttachmentPreviewProps {
  timelineId: number
  eventId: number
  attachment: Attachment
}

export function AttachmentPreview({ timelineId, eventId, attachment }: AttachmentPreviewProps) {
  const { url, loading, error } = useMediaObjectUrl(timelineId, eventId, attachment.id)

  if (loading) return <Spinner />
  if (error || !url) {
    return (
      <div className="attachment-file">
        <span>{attachment.mime_type}</span>
        <p>{error ?? 'Файл недоступен'}</p>
      </div>
    )
  }

  if (isVideoMime(attachment.mime_type)) {
    return <VideoPreview src={url} caption={attachment.caption} />
  }

  if (isImageMime(attachment.mime_type)) {
    return <ImagePreview src={url} alt={attachment.caption ?? 'Вложение'} />
  }

  return (
    <div className="attachment-file">
      <a href={url} target="_blank" rel="noreferrer">
        {attachment.caption ?? attachment.mime_type}
      </a>
    </div>
  )
}
