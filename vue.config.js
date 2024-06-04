const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,

  devServer: {
    port: 8080, // 端口号
    open:  false, // 配置自动启动浏览器
    client: {
      overlay: false //关闭异常遮罩层
    },
  },
})