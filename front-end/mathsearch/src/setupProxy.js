const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    '/api/math',
    createProxyMiddleware({
      target: 'https://math.vercel.app',
      changeOrigin: true,
      pathRewrite: { '^/api/math': '' },
    })
  );
};
