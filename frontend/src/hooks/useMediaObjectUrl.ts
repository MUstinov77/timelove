import { useEffect, useState } from 'react'
import { attachmentService } from '@/services/attachmentService'

interface MediaState {
  url: string | null
  loading: boolean
  error: string | null
}

/**
 * Загружает файл вложения (защищённый эндпоинт, требует Bearer-токен)
 * как blob и отдаёт временный object URL для <img> / <video>.
 * Object URL освобождается при размонтировании или смене вложения.
 */
export function useMediaObjectUrl(
  timelineId: number,
  eventId: number,
  attachmentId: number,
): MediaState {
  const [state, setState] = useState<MediaState>({
    url: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    let cancelled = false
    let objectUrl: string | null = null

    setState({ url: null, loading: true, error: null })

    attachmentService
      .fetchFileObjectUrl(timelineId, eventId, attachmentId)
      .then((url) => {
        objectUrl = url
        if (cancelled) {
          URL.revokeObjectURL(url)
          return
        }
        setState({ url, loading: false, error: null })
      })
      .catch((err: unknown) => {
        if (cancelled) return
        setState({
          url: null,
          loading: false,
          error: err instanceof Error ? err.message : 'Не удалось загрузить файл',
        })
      })

    return () => {
      cancelled = true
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [timelineId, eventId, attachmentId])

  return state
}
