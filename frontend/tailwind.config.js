/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          50: '#edf6f2',
          100: '#d5ece1',
          200: '#acdcc6',
          300: '#7ec6a6',
          400: '#52ac86',
          500: '#32906b',
          600: '#227354',
          700: '#1a5b43',
          800: '#144936',
          900: '#0d4734',
          950: '#06291d',
        },
        sage: {
          50: '#f4f6f4',
          100: '#e5eae5',
          200: '#ccd6cc',
          300: '#a7bcaa',
          400: '#7f9f83',
          500: '#5f8263',
          600: '#49674c',
          700: '#3a513d',
          800: '#304233',
          900: '#28362b',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
