import { useOutletContext } from 'react-router-dom'
import type { Timeline } from '@/types/timeline'

export interface TimelineOutletContext {
  /** Загруженный таймлайн текущего раздела `/timelines/:timelineId`. */
  timeline: Timeline
  /** Перезагрузить таймлайн (например, после переименования). */
  refreshTimeline: () => Promise<void>
}

/**
 * Доступ к таймлайну, загруженному в `TimelineLayout`. Работает только
 * внутри маршрутов, вложенных в `/timelines/:timelineId`.
 */
export function useTimelineContext(): TimelineOutletContext {
  return useOutletContext<TimelineOutletContext>()
}
