const { defineConfig } = require('@vue/cli-service')
const dotenv = require('dotenv')
const axios = require('axios')
const dotenvExpand = require('dotenv-expand')

var myEnv = dotenv.config({path: '../.env'})
dotenvExpand(myEnv)

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: process.env.VUE_DEV_HOST,
    port: process.env.VUE_DEV_PORT,
    proxy: {
      '^/admin': {
      target: process.env.VUE_APP_API_URL,
      changeOrigin: true,
      },
    }
  }
})
