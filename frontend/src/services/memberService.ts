import { timelineService } from '@/services/timelineService'
import type { InviteMemberPayload } from '@/types/member'

export const memberService = {
  invite(timelineId: number, payload: InviteMemberPayload) {
    return timelineService.inviteMember(timelineId, payload)
  },
}
