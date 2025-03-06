/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}', './components/*'],
  theme: {
    extend: {
      transitionProperty: {
        width: 'width',
        position: 'position',
        translate: 'translate'
      }
    }
  },
  plugins: []
}
