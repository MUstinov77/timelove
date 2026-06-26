import { Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/Button'

export function Header() {
  const { user, logout } = useAuth()

  return (
    <header className="header">
      <Link to="/" className="header-logo">
        Timeline
      </Link>
      <div className="header-user">
        {user && <span className="header-email">{user.email}</span>}
        <Button variant="ghost" onClick={logout}>
          Выйти
        </Button>
      </div>
    </header>
  )
}
