// https://umijs.org/config/
import { defineConfig } from 'umi';
import FileManagerPlugin from 'filemanager-webpack-plugin';
import defaultSettings from './defaultSettings';
import proxy from './proxy';
import routes from './routes';

const { REACT_APP_ENV, BUILD_TYPE, SERVER_URL, NODE_ENV } = process.env;

const getArgs = () => {
  const args: Record<string, any> = {};
  process.argv.splice(2).map(d => {
    const [key, value] = d?.split('=') || [];
    args[key] = value;
  });
  return args;
}


const IS_DEV = NODE_ENV === 'development';

export default defineConfig({
  publicPath: BUILD_TYPE === 'gitlab' ? '/JSJYY-houpingjia-client-page/' : '/',
  base: BUILD_TYPE === 'gitlab' ? '/JSJYY-houpingjia-client-page/' : '/',
  outputPath: 'dist/dist',
  define: {
    SERVER_URL,
    IS_DEV
  },
  hash: true,
  antd: {},
  dva: {
    hmr: true,
  },
  plugins: [],
  layout: {
    // https://umijs.org/zh-CN/plugins/plugin-layout
    locale: true,
    siderWidth: 208,
    ...defaultSettings,
  },
  // https://umijs.org/zh-CN/plugins/plugin-locale
  locale: {
    // default zh-CN
    default: 'zh-CN',
    antd: true,
    // default true, when it is true, will use `navigator.language` overwrite default
    baseNavigator: true,
  },
  dynamicImport: {
    loading: '@ant-design/pro-layout/es/PageLoading',
  },
  targets: {
    ie: 11,
  },
  // umi routes: https://umijs.org/docs/routing
  routes,
  // Theme for antd: https://ant.design/docs/react/customize-theme-cn
  theme: {
    'primary-color': defaultSettings.primaryColor,
    'link-color': '#1890FF',
    'tag-default-bg': '#EDFFFE',
    'checkbox-color': '#1890FF'
  },
  // esbuild is father build tools
  // https://umijs.org/plugins/plugin-esbuild
  esbuild: {},
  title: false,
  ignoreMomentLocale: true,
  proxy: proxy[REACT_APP_ENV || 'dev'],
  manifest: {
    basePath: '/',
  },
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
    // {
    //   requestLibPath: "import { request } from 'umi'",
    //   schemaPath: 'https://gw.alipayobjects.com/os/antfincdn/CA1dOm%2631B/openapi.json',
    //   projectName: 'swagger',
    // },
  ],
  nodeModulesTransform: {
    type: 'none',
  },
  mfsu: false,
  webpack5: {},
  exportStatic: {},
  chainWebpack: (memo, {env}) => {
    const {zip} = getArgs()
    console.log(zip, '-----')
    memo
      .when(!!zip, config => {
        config
          .plugin('zip')
          .use(FileManagerPlugin, [{
            events: {
              onEnd: {
                archive: [
                  { source: './dist/dist', destination: `./dist/${zip}.zip` },
                ],
              }
            }
          }]);
      })
  },
});
