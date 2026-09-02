import { apiClient, listOrEmpty } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { Event, EventCreatePayload, EventUpdatePayload } from '@/types/event'

export const eventService = {
  getAll(timelineId: number): Promise<Event[]> {
    return listOrEmpty(
      apiClient.get(endpoints.timeline.events(timelineId)).then((r) => r.data),
    )
  },

  getById(timelineId: number, eventId: number): Promise<Event> {
    return apiClient.get(endpoints.timeline.event(timelineId, eventId)).then((r) => r.data)
  },

  create(timelineId: number, payload: EventCreatePayload): Promise<Event> {
    return apiClient.post(endpoints.timeline.events(timelineId), payload).then((r) => r.data)
  },

  update(timelineId: number, eventId: number, payload: EventUpdatePayload): Promise<Event> {
    return apiClient
      .patch(endpoints.timeline.event(timelineId, eventId), payload)
      .then((r) => r.data)
  },

  delete(timelineId: number, eventId: number): Promise<void> {
    return apiClient.delete(endpoints.timeline.event(timelineId, eventId)).then(() => undefined)
  },
}
