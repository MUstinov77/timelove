import { useNavigate } from 'react-router-dom'
import { PageContainer } from '@/components/layout/AppLayout'
import { TimelineForm } from '@/components/timeline/TimelineForm'
import { timelineService } from '@/services/timelineService'
import type { TimelineCreatePayload } from '@/types/timeline'

export function TimelineCreatePage() {
  const navigate = useNavigate()

  const handleSubmit = async (data: TimelineCreatePayload) => {
    const timeline = await timelineService.create(data)
    navigate(`/timelines/${timeline.id}`)
  }

  return (
    <PageContainer title="Новый таймлайн">
      <TimelineForm submitLabel="Создать" onSubmit={handleSubmit} />
    </PageContainer>
  )
}
