import { getMediaUrl, isImageMime, isVideoMime } from '@/utils/getMediaUrl'
import { ImagePreview } from '@/components/attachment/ImagePreview'
import { VideoPreview } from '@/components/attachment/VideoPreview'
import type { Attachment } from '@/types/attachment'

interface AttachmentPreviewProps {
  attachment: Attachment
}

export function AttachmentPreview({ attachment }: AttachmentPreviewProps) {
  const url = getMediaUrl(attachment.id)

  if (isVideoMime(attachment.mime_type)) {
    return <VideoPreview src={url} caption={attachment.caption} />
  }

  if (isImageMime(attachment.mime_type)) {
    return <ImagePreview src={attachment.storage_key} alt={attachment.caption ?? 'Вложение'} />
  }

  return (
    <div className="attachment-file">
      <span>{attachment.mime_type}</span>
      {attachment.caption && <p>{attachment.caption}</p>}
    </div>
  )
}
