import type { Settings as LayoutSettings } from '@ant-design/pro-layout';
import { PageLoading } from '@ant-design/pro-layout';
import type { RunTimeLayoutConfig, RequestConfig } from 'umi';
import { history, Link } from 'umi';
import _ from 'lodash';
import RightContent from '@/components/RightContent';
import Footer from '@/components/Footer';
import { getDicts, queryCurrentUser } from './services/main';
import { BookOutlined, LinkOutlined } from '@ant-design/icons';
import { array2Map } from '@/util/array2Map';
import paramFormat from '@/util/paramFormat'
import localStorage, { keys } from '@/util/localStorage';

const isDev = process.env.NODE_ENV === 'development';
// const serverUrl = process.env.SERVER_URL; // 指定服务地址
const loginPath = '/user/login';

/** 获取用户信息比较慢的时候会展示一个 loading */
export const initialStateConfig = {
  loading: <PageLoading />,
};

/**
 * @see  https://umijs.org/zh-CN/plugins/plugin-initial-state
 * */
export async function getInitialState(): Promise<{
  settings?: Partial<LayoutSettings>;
  currentUser?: Record<string, any>;
  fetchUserInfo?: () => Promise<Record<string, any>|undefined>;
  dicts: API.DictsMap;
}> {
  const userName = localStorage.getItem(keys.USER_NAME);
  const fetchUserInfo = async () => {
    if (!userName) {
      return;
    }
    try {
      const msg = await queryCurrentUser();
      if (_.isNil(msg.data?.user_name)) {
        throw Error('未获取到用户信息');
      }
      return {
        name: msg.data?.user_name
      } as Record<string, any>;
    } catch (error) {
      console.error(error)
    }
    return;
  };
  const fetchDicts = async (): Promise<API.DictsMap> => {
    if (userName) {
      try {
        const msg = await getDicts();
        return {
          classification: array2Map(msg?.data?.classification) || {},
          voltage_level: array2Map(msg?.data?.voltage_level) || {},
        };
      } catch (error) {}
    }
    return {
      classification: {},
      voltage_level: {},
    };
  };
  // 如果是登录页面，不执行
  if (history.location.pathname !== loginPath) {
    const currentUser = await fetchUserInfo();
    const dicts = await fetchDicts();
    return {
      fetchUserInfo,
      currentUser,
      settings: {},
      dicts,
    };
  }
  return {
    fetchUserInfo,
    settings: {},
    dicts: {
      classification: {},
      voltage_level: {},
    }
  };
}

// ProLayout 支持的api https://procomponents.ant.design/components/layout
export const layout: RunTimeLayoutConfig = ({ initialState }) => {
  return {
    rightContentRender: () => <RightContent />,
    disableContentMargin: false,
    // waterMarkProps: {
    //   content: initialState?.currentUser?.name,
    // },
    footerRender: () => null && <Footer />,
    onPageChange: () => {
      const { location } = history;
      // 如果没有登录，重定向到 login
      if (!initialState?.currentUser && location.pathname !== loginPath) {
        history.push(loginPath);
      }
    },
    links: isDev
      ? [
          <Link to="/umi/plugin/openapi" target="_blank">
            <LinkOutlined />
            <span>OpenAPI 文档</span>
          </Link>,
          <Link to="/~docs">
            <BookOutlined />
            <span>业务组件文档</span>
          </Link>,
        ]
      : [],
    menuHeaderRender: () => (
      <div>
        <img src={require('@/assets/logo.png')} alt="" />
      </div>
    ),
    // 自定义 403 页面
    // unAccessible: <div>unAccessible</div>,
    ...initialState?.settings,
  };
};

export const request: RequestConfig = {
  errorConfig: {
    adaptor: (resData) => {
      console.log( '%c 接口响应:', 'font-size: 16px; color: red', resData)
    // if(resData instanceof Blob){
    //  return{
    //   ...resData,
    //  }
    // }
      return {
        ...resData,
        success: resData.code ? resData.code === 'SUCCESS' : true, // XXX: 这里没有code和 等于SUCCESS的都认为成功，如果其他情况需要使用通用报错的，主动throw错误
        errorMessage: resData.message || '请求错误，请稍后重试！',
      };
    },
  },
  middlewares: [
    async function middlewareA(ctx, next) {
      try {
        await next();
      } catch(err: any) {
        throw new Error(err.message || '请求错误，请稍后重试！');
      }
    },
  ],
  responseInterceptors: [
    // 401 认证失效
    async(response) => {
      if (response.status === 401) {
        history.push(loginPath);
        throw new Error('登录失效，请重新登录！');
      }
      return response;
    },
    // 拿出total
    async (response) => {
      if ((response.url||'').endsWith('/api/v1/comment/download')) {
        return response
      }
      const data = await response.clone().json();
      return {
        total: data?.data?.total || 0,
        ...data||{},
      }
    }
  ],
  requestInterceptors: [
    (url, options) => {
      console.log(options, url)
      return {
        url,
        options: paramFormat(options),
      };
    },
  ],
  prefix: SERVER_URL || (isDev ? '/devProxy/api/v1' : '/api/v1')
};
