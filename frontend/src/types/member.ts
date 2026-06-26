export const MemberPermission = {
  Member: 'MEMBER',
  Moderator: 'MODERATOR',
  Admin: 'ADMIN',
} as const

export type MemberPermission = (typeof MemberPermission)[keyof typeof MemberPermission]

export interface InviteMemberPayload {
  member_id: number
  member_permission: MemberPermission
}
