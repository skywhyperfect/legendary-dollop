/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        wa: {
          light: '#efeae2',
          header: '#f0f2f5',
          green: '#25D366',
          dark: '#111b21',
          panel: '#202c33'
        }
      }
    },
  },
  plugins: [],
}
