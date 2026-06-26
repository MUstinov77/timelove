import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '@/components/layout/AppLayout'
import { LoginPage } from '@/pages/auth/LoginPage'
import { SignupPage } from '@/pages/auth/SignupPage'
import { EventCreatePage } from '@/pages/events/EventCreatePage'
import { EventDetailPage } from '@/pages/events/EventDetailPage'
import { EventEditPage } from '@/pages/events/EventEditPage'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { TimelineCreatePage } from '@/pages/timelines/TimelineCreatePage'
import { TimelineDetailPage } from '@/pages/timelines/TimelineDetailPage'
import { TimelineListPage } from '@/pages/timelines/TimelineListPage'
import { GuestRoute } from '@/routes/GuestRoute'
import { ProtectedRoute } from '@/routes/ProtectedRoute'

export const router = createBrowserRouter([
  {
    element: <GuestRoute />,
    children: [
      { path: '/login', element: <LoginPage /> },
      { path: '/signup', element: <SignupPage /> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { index: true, element: <TimelineListPage /> },
          { path: 'timelines/new', element: <TimelineCreatePage /> },
          { path: 'timelines/:timelineId', element: <TimelineDetailPage /> },
          { path: 'timelines/:timelineId/events/new', element: <EventCreatePage /> },
          { path: 'timelines/:timelineId/events/:eventId', element: <EventDetailPage /> },
          { path: 'timelines/:timelineId/events/:eventId/edit', element: <EventEditPage /> },
        ],
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
])
