import { createContext, useCallback, useMemo, useState, type ReactNode } from 'react'
import { authService } from '@/services/authService'
import type { AuthUser, LoginPayload, SignupPayload } from '@/types/auth'
import { decodeJwt } from '@/utils/decodeJwt'
import { tokenStorage } from '@/utils/tokenStorage'

interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  isAuthenticated: boolean
  login: (payload: LoginPayload) => Promise<void>
  signup: (payload: SignupPayload) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)

function userFromToken(token: string): AuthUser {
  const payload = decodeJwt(token)
  return {
    userId: payload.context.user_id,
    email: payload.context.username,
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const storedToken = tokenStorage.get()
  const [token, setToken] = useState<string | null>(storedToken)
  const [user, setUser] = useState<AuthUser | null>(() =>
    storedToken ? userFromToken(storedToken) : null,
  )

  const setAuth = useCallback((accessToken: string) => {
    tokenStorage.set(accessToken)
    setToken(accessToken)
    setUser(userFromToken(accessToken))
  }, [])

  const login = useCallback(
    async (payload: LoginPayload) => {
      const { access_token } = await authService.login(payload)
      setAuth(access_token)
    },
    [setAuth],
  )

  const signup = useCallback(async (payload: SignupPayload) => {
    await authService.signup(payload)
  }, [])

  const logout = useCallback(() => {
    tokenStorage.remove()
    setToken(null)
    setUser(null)
  }, [])

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: !!token,
      login,
      signup,
      logout,
    }),
    [user, token, login, signup, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
