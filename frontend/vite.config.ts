import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The backend (problem 7) allows exactly this origin, so keep the port fixed.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
});
