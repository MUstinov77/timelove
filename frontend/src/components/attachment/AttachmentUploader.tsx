import { useCallback, useRef, useState } from 'react'
import { useFileUpload } from '@/hooks/useFileUpload'
import { Button } from '@/components/ui/Button'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import type { Attachment } from '@/types/attachment'

interface AttachmentUploaderProps {
  timelineId: number
  eventId: number
  onUploaded?: (attachments: Attachment[]) => void
}

export function AttachmentUploader({ timelineId, eventId, onUploaded }: AttachmentUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)
  const { upload, progress, uploading, error } = useFileUpload(timelineId, eventId)

  const handleFiles = useCallback(
    async (files: FileList | null) => {
      if (!files || files.length === 0) return
      const results = await upload(Array.from(files))
      onUploaded?.(results)
    },
    [upload, onUploaded],
  )

  return (
    <div className="attachment-uploader">
      <div
        className={`upload-zone ${dragOver ? 'upload-zone--active' : ''}`}
        onDragOver={(e) => {
          e.preventDefault()
          setDragOver(true)
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragOver(false)
          void handleFiles(e.dataTransfer.files)
        }}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        <p>Перетащите фото или видео сюда</p>
        <p className="upload-zone-hint">JPEG, PNG, WebP, MP4, WebM</p>
        <Button type="button" variant="secondary" disabled={uploading}>
          Выбрать файлы
        </Button>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept="image/jpeg,image/png,image/webp,video/mp4,video/webm"
          hidden
          onChange={(e) => void handleFiles(e.target.files)}
        />
      </div>

      {uploading && (
        <div className="upload-progress">
          <div className="upload-progress-bar" style={{ width: `${progress}%` }} />
          <span>{progress}%</span>
        </div>
      )}

      {error && <ErrorMessage message={error} />}
    </div>
  )
}
