import { apiClient, listOrEmpty } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { MessageResponse } from '@/types/api'
import type { InviteMemberPayload } from '@/types/member'
import type { Timeline, TimelineCreatePayload } from '@/types/timeline'

export const timelineService = {
  getAll(): Promise<Timeline[]> {
    return listOrEmpty(apiClient.get(endpoints.timeline.list).then((r) => r.data))
  },

  getById(timelineId: number): Promise<Timeline> {
    return apiClient.get(endpoints.timeline.detail(timelineId)).then((r) => r.data)
  },

  create(payload: TimelineCreatePayload): Promise<Timeline> {
    return apiClient.post(endpoints.timeline.list, payload).then((r) => r.data)
  },

  update(timelineId: number, payload: TimelineCreatePayload): Promise<Timeline> {
    return apiClient.patch(endpoints.timeline.detail(timelineId), payload).then((r) => r.data)
  },

  delete(timelineId: number): Promise<void> {
    return apiClient.delete(endpoints.timeline.detail(timelineId)).then(() => undefined)
  },

  inviteMember(timelineId: number, payload: InviteMemberPayload): Promise<MessageResponse> {
    return apiClient.post(endpoints.timeline.addMember(timelineId), payload).then((r) => r.data)
  },
}
