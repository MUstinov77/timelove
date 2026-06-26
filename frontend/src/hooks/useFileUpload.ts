import { useCallback, useState } from 'react'
import { attachmentService } from '@/services/attachmentService'
import type { Attachment } from '@/types/attachment'

const ACCEPTED_TYPES = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'video/mp4',
  'video/webm',
]

export function useFileUpload(timelineId: number, eventId: number) {
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const validateFiles = useCallback((files: File[]) => {
    const invalid = files.filter((f) => !ACCEPTED_TYPES.includes(f.type))
    if (invalid.length > 0) {
      throw new Error(`Неподдерживаемый формат: ${invalid.map((f) => f.name).join(', ')}`)
    }
  }, [])

  const upload = useCallback(
    async (files: File[], caption?: string): Promise<Attachment[]> => {
      validateFiles(files)
      setUploading(true)
      setError(null)
      setProgress(0)

      const results: Attachment[] = []
      try {
        for (const file of files) {
          const attachment = await attachmentService.upload(
            timelineId,
            eventId,
            file,
            caption,
            setProgress,
          )
          results.push(attachment)
        }
        return results
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Ошибка загрузки'
        setError(message)
        throw err
      } finally {
        setUploading(false)
        setProgress(0)
      }
    },
    [timelineId, eventId, validateFiles],
  )

  return { upload, progress, uploading, error }
}
