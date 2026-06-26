export interface Event {
  id: number
  title: string
  event_date: string
  description: string
}

export interface EventCreatePayload {
  title: string
  event_date: string
  description: string
}

export type EventUpdatePayload = Partial<EventCreatePayload>
