import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    open: true,
  },
  preview: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    open: true,
  },
})
