export const endpoints = {
  health: '/',
  auth: {
    signup: '/auth/signup',
    login: '/auth/login',
  },
  timeline: {
    list: '/timeline/',
    detail: (id: number) => `/timeline/${id}`,
    addMember: (id: number) => `/timeline/${id}/add`,
    events: (timelineId: number) => `/timeline/${timelineId}/event/`,
    event: (timelineId: number, eventId: number) =>
      `/timeline/${timelineId}/event/${eventId}`,
    attachments: (timelineId: number, eventId: number) =>
      `/timeline/${timelineId}/event/${eventId}/attachment/`,
    attachment: (timelineId: number, eventId: number, attachmentId: number) =>
      `/timeline/${timelineId}/event/${eventId}/attachment/${attachmentId}`,
  },
} as const
