interface ImagePreviewProps {
  src: string
  alt: string
}

export function ImagePreview({ src, alt }: ImagePreviewProps) {
  return (
    <div className="attachment-image">
      <img src={src} alt={alt} loading="lazy" />
    </div>
  )
}
