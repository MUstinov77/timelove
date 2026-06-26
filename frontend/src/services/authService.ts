import { apiClient } from '@/api/client'
import { endpoints } from '@/api/endpoints'
import type { LoginPayload, SignupPayload, TokenResponse } from '@/types/auth'
import type { MessageResponse } from '@/types/api'

export const authService = {
  signup(payload: SignupPayload): Promise<MessageResponse> {
    return apiClient.post(endpoints.auth.signup, payload).then((r) => r.data)
  },

  login(payload: LoginPayload): Promise<TokenResponse> {
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
