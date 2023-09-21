/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  mode: 'jit',
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
        colors: {
            darkBg: '#121212',
            darkText: '#E4E4E4',
            darkSidebar: '#1E1E1E',
            darkContent: '#242424',
            primary: '#2C5282',
            secondary: '#4A90E2',
            'secondary-hover': '#357ABD',  // Slightly darker shade for hover effect
            success: '#48BB78',
            'success-hover': '#2F855A',    // Slightly darker shade for hover effect
            neutralDark: '#2D3748',
            neutralLight: '#EDF2F7'
        },
    },
  },
  variants: {},
  plugins: [],
}

