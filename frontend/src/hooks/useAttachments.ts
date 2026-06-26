import { useCallback, useEffect, useState } from 'react'
import { attachmentService } from '@/services/attachmentService'
import type { Attachment, AttachmentUpdatePayload } from '@/types/attachment'

export function useAttachments(timelineId: number, eventId: number) {
  const [attachments, setAttachments] = useState<Attachment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await attachmentService.getAll(timelineId, eventId)
      setAttachments(data.sort((a, b) => a.sort_order - b.sort_order))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить вложения')
    } finally {
      setLoading(false)
    }
  }, [timelineId, eventId])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const upload = useCallback(
    async (file: File, caption?: string, onProgress?: (percent: number) => void) => {
      const attachment = await attachmentService.upload(
        timelineId,
        eventId,
        file,
        caption,
        onProgress,
      )
      setAttachments((prev) => [...prev, attachment])
      return attachment
    },
    [timelineId, eventId],
  )

  const update = useCallback(
    async (attachmentId: number, payload: AttachmentUpdatePayload) => {
      const attachment = await attachmentService.update(
        timelineId,
        eventId,
        attachmentId,
        payload,
      )
      setAttachments((prev) => prev.map((a) => (a.id === attachmentId ? attachment : a)))
      return attachment
    },
    [timelineId, eventId],
  )

  const remove = useCallback(
    async (attachmentId: number) => {
      await attachmentService.delete(timelineId, eventId, attachmentId)
      setAttachments((prev) => prev.filter((a) => a.id !== attachmentId))
    },
    [timelineId, eventId],
  )

  return { attachments, loading, error, refresh, upload, update, remove }
}
