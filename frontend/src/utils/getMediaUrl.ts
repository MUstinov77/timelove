import { AttachmentType } from '@/types/attachment'

export function getMediaUrl(
    attachmentId: number
): string {
  const base = import.meta.env.VITE_API_BASE_URL ?? ''
  return `${base}/attachment/${attachmentId}/file`
}

export function resolveMediaType(mimeType: string): AttachmentType {
  if (mimeType.startsWith('video/')) return AttachmentType.Video
  if (mimeType.startsWith('audio/')) return AttachmentType.Audio
  return AttachmentType.Image
}

export function isImageMime(mimeType: string): boolean {
  return mimeType.startsWith('image/')
}

export function isVideoMime(mimeType: string): boolean {
  return mimeType.startsWith('video/')
}
