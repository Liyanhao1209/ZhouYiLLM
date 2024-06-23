const url = require('./config/config')
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,

  devServer: {
    port: 8080, // 端口号
    open: false, // 配置自动启动浏览器
    client: {
      overlay: false //关闭异常遮罩层
    },
    allowedHosts: "all",
    proxy: { // 跨域
      "/api": {
        target: url,
        changeOrigin: true,
        // ws: true,//websocket支持
        secure: true,
        ws: false,
        pathRewrite: {
          "^/api": ""
        }
      },
    }
  },
})