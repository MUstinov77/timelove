import path from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Запросы к API идут напрямую на VITE_API_BASE_URL (см. src/api/client.ts),
// CORS на бэкенде открыт — dev-прокси не нужен. Прежний прокси на префикс
// '/timeline' перехватывал и SPA-маршруты '/timelines/...', ломая перезагрузку.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
  },
})
