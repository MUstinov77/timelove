import type { Attachment } from '@/types/attachment'
import type { Event } from '@/types/event'

export interface EventWithAttachments extends Event {
  attachments: Attachment[]
}

export interface TimelineEventView extends Event {
  attachmentCount: number
  coverAttachment?: Attachment
}
