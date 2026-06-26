export interface ApiError {
  detail: string | { msg: string; type: string }[]
  status: number
}

export interface MessageResponse {
  message: string
}
