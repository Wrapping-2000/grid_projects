//路由
export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './user/Login',
          },
        ],
      },
      {
        component: './404',
      },
    ],
  },
  {
    path: '/project',
    component: '@/layouts/index',
    //flatMenu: true,
    name: 'project',
    routes: [
      {
        path: '/project',
        redirect: '/project/list',
      },
      {
        path: '/project/list',
        name: 'project-list',
        component: './project/list',
      },
      {
        path: '/project/summary',
        name: 'project-summary',
        component: './project/summary',
      },
      {
        component: './404',
      },
    ],
  },
  {
    path: '/visualContainer',
    name: 'visualContainer',
    component: '@/layouts/index',
    routes: [
      {
        path: '/visualContainer',
        redirect: '/visualContainer/list',
      },
      {
        path: '/visualContainer/list',
        name: 'visualContainer-list',
        component: './visualContainer/list',
      },
      {
        path: '/visualContainer/dataSources',
        name: 'visualContainer-dataSources',
        component: './visualContainer/dataSources',
      },
      {
        component: './404',
      },
    ],
  },
  {
    path: '/visualResult',
    icon: 'crown',
    component: '@/layouts/index',
    flatMenu: true,
    routes: [
      {
        path: '/visualResult',
        redirect: '/visualResult/list',
      },
      {
        path: '/visualResult/list',
        component: './visualResult/list',
      },
      {
        component: './404',
      },
    ],
  },
  {
    path: '/',
    redirect: '/project',
  },
  {
    component: './404',
  },
];
