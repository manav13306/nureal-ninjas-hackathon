/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#111827',
        primary: '#3b82f6',
        accent: '#ef4444'
      }
    },
  },
  plugins: [],
}
