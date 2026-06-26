import { Link } from 'react-router-dom'
import { PageContainer } from '@/components/layout/AppLayout'
import { TimelineCard } from '@/components/timeline/TimelineCard'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/ui/EmptyState'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Spinner } from '@/components/ui/Spinner'
import { useTimelines } from '@/hooks/useTimelines'

export function TimelineListPage() {
  const { timelines, loading, error } = useTimelines()

  return (
    <PageContainer
      title="Мои таймлайны"
      actions={
        <Link to="/timelines/new">
          <Button>+ Создать</Button>
        </Link>
      }
    >
      {loading && <Spinner />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && timelines.length === 0 && (
        <EmptyState
          title="Пока нет таймлайнов"
          description="Создайте первый таймлайн для ваших событий"
          action={
            <Link to="/timelines/new">
              <Button>Создать таймлайн</Button>
            </Link>
          }
        />
      )}
      <div className="timeline-grid">
        {timelines.map((timeline) => (
          <TimelineCard key={timeline.id} timeline={timeline} />
        ))}
      </div>
    </PageContainer>
  )
}
