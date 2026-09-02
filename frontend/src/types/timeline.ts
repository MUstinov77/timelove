import type { MemberPermission } from '@/types/member'

export interface Timeline {
  id: number
  title: string
  /** Роль текущего пользователя в этом таймлайне (отдаёт бэкенд). */
  member_permission: MemberPermission
}

export interface TimelineCreatePayload {
  title: string
}
