import { AttachmentType } from '@/types/attachment'

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
