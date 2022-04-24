const colors = require('tailwindcss/colors')

module.exports = {
  mode: 'jit',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    fontFamily: {
      sans: ['Roboto'],
      sansTitle: ['RobotoCondensed'],
      sansThin: ['RobotoThin'],
      letter: ['RozhaOne'],
    },
  },
  plugins: [],
}
