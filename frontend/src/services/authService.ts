import { apiClient } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { LoginPayload, SignupPayload, TokenResponse } from '@/types/auth'
import type { MessageResponse } from '@/types/api'

export const authService = {
  signup(payload: SignupPayload): Promise<MessageResponse> {
    // Бэкенд (UserSignupSchema) требует, чтобы поля first_name / last_name
    // присутствовали в теле запроса, пусть даже со значением null.
    const body = {
      email: payload.email,
      password: payload.password,
      first_name: payload.first_name?.trim() || null,
      last_name: payload.last_name?.trim() || null,
    }
    return apiClient.post(endpoints.auth.signup, body).then((r) => r.data)
  },

  login(payload: LoginPayload): Promise<TokenResponse> {
    // POST /auth/login ожидает OAuth2PasswordRequestForm:
    // form-urlencoded с полями username / password.
    const form = new URLSearchParams()
    form.append('username', payload.email)
    form.append('password', payload.password)

    return apiClient
      .post(endpoints.auth.login, form, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      .then((r) => r.data)
  },
}
