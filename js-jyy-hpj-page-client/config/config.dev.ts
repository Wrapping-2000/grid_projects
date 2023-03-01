// https://umijs.org/config/
import { defineConfig } from 'umi';
//import defaultSettings from './defaultSettings';
import proxy from './proxy';
//import routes from './routes';
import { DEVELOPMENT_URL } from './constants';

const { REACT_APP_ENV } = process.env;

export default defineConfig({
  ignoreMomentLocale: true,
  proxy: proxy[REACT_APP_ENV || 'dev'],
  // Fast Refresh 热更新
  fastRefresh: {},
  openAPI: [
    {
      requestLibPath: "import { request } from 'umi'",
      // 或者使用在线的版本
      schemaPath: 'http://192.168.2.123:8070/apispec_1.json',
      // schemaPath: join(__dirname, 'oneapi.json'),
      mock: false,
      projectName: 'houpingjia',
    },
  ],
  nodeModulesTransform: {
    type: 'none',
  },
  mfsu: false,
  webpack5: {},
  exportStatic: {},
  devServer: {
    proxy: {
      '/devProxy': {
        target: DEVELOPMENT_URL,
        changeOrigin: true,
        pathRewrite: { '^/devProxy': '' },
        secure: false,
        // onProxyReq: (...p) => console.log('DDDDDDDD', ...p)
      },
    },
  },
});
