import { NavLink } from 'react-router-dom'
import { useTimelines } from '@/hooks/useTimelines'
import { Spinner } from '@/components/ui/Spinner'

export function Sidebar() {
  const { timelines, loading } = useTimelines()

  return (
    <aside className="sidebar">
      <NavLink to="/timelines/new" className="sidebar-new">
        + Новый таймлайн
      </NavLink>

      {loading ? (
        <Spinner />
      ) : (
        <nav className="sidebar-nav">
          {timelines.map((timeline) => (
            <NavLink
              key={timeline.id}
              to={`/timelines/${timeline.id}`}
              className={({ isActive }) => `sidebar-link ${isActive ? 'sidebar-link--active' : ''}`}
            >
              {timeline.title}
            </NavLink>
          ))}
        </nav>
      )}
    </aside>
  )
}
