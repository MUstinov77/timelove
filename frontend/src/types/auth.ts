export interface SignupPayload {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: 'bearer'
}

export interface AuthUser {
  userId: number
  email: string
}

export interface JwtPayload {
  context: {
    user_id: number
    username: string
  }
}
