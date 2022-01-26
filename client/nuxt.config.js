import colors from 'vuetify/es5/util/colors'
const env = require('dotenv').config()

export default {
  // Global page header: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s',
    title: 'Simple Additions (Find Animal Shelters Near You)',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content:
          "Simple Addidtions the project I'm using to show off my ability to create a responsive and interactive frontend webpage as well as a secure and comprehensive backend database."
      },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/saLogo.png' },
      { rel: 'apple-touch-icon', type: 'image/x-icon', href: '/saLogo.png' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [],

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      default: false,
      themes: {
        default: {},
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  privateRuntimeConfig: {
    secretKey: process.env.SECRET_KEY,
    apiAddress: process.env.API_ADDRESS
  },

  target: 'static'
}
