import { apiClient } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { Attachment, AttachmentUpdatePayload } from '@/types/attachment'

export const attachmentService = {
  getAll(timelineId: number, eventId: number): Promise<Attachment[]> {
    return apiClient.get(endpoints.timeline.attachments(timelineId, eventId)).then((r) => r.data)
  },

  getById(timelineId: number, eventId: number, attachmentId: number): Promise<Attachment> {
    return apiClient
      .get(endpoints.timeline.attachment(timelineId, eventId, attachmentId))
      .then((r) => r.data)
  },

  upload(
    timelineId: number,
    eventId: number,
    file: File,
    caption?: string,
    onProgress?: (percent: number) => void,
  ): Promise<Attachment> {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient
      .post(endpoints.timeline.attachments(timelineId, eventId), formData, {
        params: caption ? { caption } : undefined,
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (event) => {
          if (onProgress && event.total) {
            onProgress(Math.round((event.loaded * 100) / event.total))
          }
        },
      })
      .then((r) => r.data)
  },

  update(
    timelineId: number,
    eventId: number,
    attachmentId: number,
    payload: AttachmentUpdatePayload,
  ): Promise<Attachment> {
    return apiClient
      .patch(endpoints.timeline.attachment(timelineId, eventId, attachmentId), payload)
      .then((r) => r.data)
  },

  delete(timelineId: number, eventId: number, attachmentId: number): Promise<void> {
    return apiClient
      .delete(endpoints.timeline.attachment(timelineId, eventId, attachmentId))
      .then(() => undefined)
  },
}
