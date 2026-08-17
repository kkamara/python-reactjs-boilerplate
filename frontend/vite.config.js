import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig(() => {
  return {
    plugins: [react()],
    base: "/static/",
    server: {
      host: "localhost",
      port: 5173,
      cors: true,
    },
    preview: {
      host: "localhost",
      port: 5173,
      cors: true,
    },
    build: {
      manifest: "manifest.json",
      rollupOptions: {
        input: "src/index.jsx",
      },
    },
    test: {
      globals: true,
      environment: "jsdom",
      setupFiles: "./src/setupTests.js",
      include: ["src/**/*.test.{js,jsx}"],
    },
  }
})