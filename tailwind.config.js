/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "**/*.html",
  ],
  darkMode: "class",
  theme: {
    extend: {
      backgroundImage: {
        'background-dark-lg': "url('/static/img/background-dark.svg')",
        'background-dark-sm': "url('/static/img/background-dark-sm.svg')",
        'background-light-lg': "url('/static/img/background.svg')",
        'background-light-sm': "url('/static/img/background-sm.svg')",
        'logo-dark': "url('/static/img/logo-cheio-dark.png')",
        'logo-light': "url('/static/img/logo-cheio.png')",
      },
      fontFamily: {
        sans: ["Montserrat", "sans-serif"],
        subrayada: ["Montserrat Subrayada", "sans-serif"],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
  daisyui: {
    themes: [
      {
        dark: {
          ...require("daisyui/src/theming/themes")["[data-theme=dark]"],
          "primary": "#F9B233",
          "primary-content": "#281A01",
          "secondary": "#4B5CA5",
          "secondary-content": "#F1F2F9",
          "accent": "#E9501D",
          "accent-content": "#FDF1EC"
        },
      },
      {
        light: {
          ...require("daisyui/src/theming/themes")["[data-theme=light]"],
          "primary": "#62AAFF",
          "primary-content": "#001329",
          "secondary": "#97E1D4",
          "secondary-content": "#09201C",
          "accent": "#FF957D",
          "accent-content": "#290700",
          "base-100": "#F2F6FF"
        }
      }
    ]
  },
}

