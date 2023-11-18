/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*", "./templates/**/*", "./templates/auth/*", "./templates/**/*"],
  theme: {
    extend: {
      fontFamily: {
        regular: ['regular', 'sans-serif'],
        semiBold: ['semiBold', 'sans-serif']
      },
    },
  },
  plugins: [],
}