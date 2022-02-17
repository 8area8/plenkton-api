const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/static/",
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
