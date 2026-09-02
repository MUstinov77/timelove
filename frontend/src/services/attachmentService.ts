import { apiClient, listOrEmpty } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { Attachment, AttachmentUpdatePayload } from '@/types/attachment'

export const attachmentService = {
  getAll(timelineId: number, eventId: number): Promise<Attachment[]> {
    return listOrEmpty(
      apiClient.get(endpoints.timeline.attachments(timelineId, eventId)).then((r) => r.data),
    )
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
    // POST .../attachment/ — multipart/form-data: файл в поле `file`,
    // caption читается бэкендом из формы (AttachmentCreateSchema.as_form).
    const formData = new FormData()
    formData.append('file', file)
    if (caption) {
      formData.append('caption', caption)
    }

    return apiClient
      .post(endpoints.timeline.attachments(timelineId, eventId), formData, {
        // Явно указываем multipart — axios сам подставит boundary
        // вместо унаследованного от инстанса application/json.
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
    // PATCH ожидает AttachmentCreateSchema — поле caption обязательно
    // должно присутствовать (может быть null).
    const body = { caption: payload.caption ?? null }
    return apiClient
      .patch(endpoints.timeline.attachment(timelineId, eventId, attachmentId), body)
      .then((r) => r.data)
  },

  delete(timelineId: number, eventId: number, attachmentId: number): Promise<void> {
    return apiClient
      .delete(endpoints.timeline.attachment(timelineId, eventId, attachmentId))
      .then(() => undefined)
  },

  /**
   * Файл вложения отдаётся защищённым эндпоинтом (нужен Bearer-токен),
   * поэтому его нельзя подставить напрямую в <img src>. Качаем как blob
   * через axios и возвращаем object URL — вызывающий код обязан
   * освободить его через URL.revokeObjectURL.
   */
  fetchFileObjectUrl(
    timelineId: number,
    eventId: number,
    attachmentId: number,
  ): Promise<string> {
    return apiClient
      .get(endpoints.timeline.attachmentFile(timelineId, eventId, attachmentId), {
        responseType: 'blob',
      })
      .then((r) => URL.createObjectURL(r.data as Blob))
  },
}
