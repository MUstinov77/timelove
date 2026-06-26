import { useMemo } from 'react'
import { MemberPermission, type MemberPermission as MemberPermissionType } from '@/types/member'

const PERMISSION_RANK: Record<MemberPermissionType, number> = {
  [MemberPermission.Member]: 1,
  [MemberPermission.Moderator]: 2,
  [MemberPermission.Admin]: 3,
}

export function usePermissions(userPermission: MemberPermissionType = MemberPermission.Admin) {
  return useMemo(() => {
    const has = (required: MemberPermissionType) =>
      PERMISSION_RANK[userPermission] >= PERMISSION_RANK[required]

    return {
      canView: has(MemberPermission.Member),
      canCreateEvent: has(MemberPermission.Moderator),
      canEditEvent: has(MemberPermission.Moderator),
      canDeleteEvent: has(MemberPermission.Admin),
      canInvite: has(MemberPermission.Moderator),
      canDeleteTimeline: has(MemberPermission.Admin),
    }
  }, [userPermission])
}
