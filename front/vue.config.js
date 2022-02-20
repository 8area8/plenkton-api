const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.DEPLOY ? process.env.CLOUD_BASE_URL : "/static/",
  configureWebpack: {
    devServer: {
      devMiddleware: {
        index: true,
        mimeTypes: { phtml: "text/html" },
        publicPath: "./dist",
        serverSideRender: true,
        writeToDisk: true,
      },
    },
  },
});
