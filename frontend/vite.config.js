import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// https://vite.dev/config/
/** @type {import('tailwindcss').Config} */
export default defineConfig({
  plugins: [react(), tailwindcss()],
  theme: {
    extend: {
      fontFamily: {
        square: ['Square Game', 'sans-serif'],
      },
    },
  }, // Correct placement of plugins
})
