import axios, { AxiosError } from 'axios'
import { tokenStorage } from '@/utils/tokenStorage'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.get()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
 * FastAPI отдаёт ошибки в поле `detail`: строкой или массивом
 * ValidationError'ов ({ msg, loc, type }). Приводим это к читаемому
 * `error.message`, чтобы хуки могли показывать осмысленный текст.
 */
function extractDetail(error: AxiosError): string | null {
  const data = error.response?.data as
    | { detail?: string | { msg?: string }[] }
    | undefined
  const detail = data?.detail
  if (!detail) return null
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const messages = detail.map((item) => item?.msg).filter(Boolean)
    if (messages.length > 0) return messages.join(', ')
  }
  return null
}

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      tokenStorage.remove()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    const detail = extractDetail(error)
    if (detail) {
      error.message = detail
    }

    return Promise.reject(error)
  },
)

/** true, если это ошибка axios с указанным HTTP-статусом. */
export function isHttpStatus(error: unknown, status: number): boolean {
  return error instanceof AxiosError && error.response?.status === status
}

/**
 * Бэкенд для «списочных» эндпоинтов ({@link https://} `GET /timeline/`,
 * `.../event/`, `.../attachment/`) отвечает 404, если данных нет.
 * Для UI это эквивалентно пустому списку.
 */
export async function listOrEmpty<T>(request: Promise<T[]>): Promise<T[]> {
  try {
    return await request
  } catch (error) {
    if (isHttpStatus(error, 404)) return []
    throw error
  }
}
