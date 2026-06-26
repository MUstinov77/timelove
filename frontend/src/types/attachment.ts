export const AttachmentType = {
  Image: 'image',
  Video: 'video',
  Audio: 'audio',
} as const

export type AttachmentType = (typeof AttachmentType)[keyof typeof AttachmentType]

export interface Attachment {
  id: number
  media_type: AttachmentType
  mime_type: string
  storage_key: string
  thumbnail_key: string | null
  file_size: number
  width: number | null
  height: number | null
  duration_ms: number | null
  sort_order: number
  caption: string | null
  event_id: number
}

export interface AttachmentUpdatePayload {
  caption?: string
}
