interface VideoPreviewProps {
  src: string
  caption?: string | null
}

export function VideoPreview({ src, caption }: VideoPreviewProps) {
  return (
    <div className="attachment-video">
      <video src={src} controls preload="metadata" />
      {caption && <p className="attachment-caption">{caption}</p>}
    </div>
  )
}
