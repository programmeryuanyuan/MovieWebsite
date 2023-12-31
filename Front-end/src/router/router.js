
import home from '../views/home/home.vue'

import {
  createMemoryHistory,
  createRouter as _createRouter,
  createWebHistory,
  // createWebHashHistory
} from 'vue-router'

export function createRouter() {
  return _createRouter({
    // use appropriate history implementation for server/client
    // import.meta.env.SSR is injected by Vite.
    history: import.meta.env.SSR ? createMemoryHistory('/') : createWebHistory('/'),
    routes:[
      { path: '/', redirect: '/home' },// 配置默认路由，重定向到/home
      { path: '/home', component: home },
      { path: '/detail', component:() => import('../views/detail/detail.vue') },
      { path: '/detailInfo/:id', component: () => import('../views/detail/detailInfo.vue')},
      { path: '/publish', component:() => import('../views/publish/publish.vue') },
      { path: '/login', component:() => import('../views/login/login.vue') },
      { path: '/search', component:() => import('../views/search/search.vue') },
      { path: '/register', component:() => import('../views/login/register.vue') },
      { path: '/info', component:() => import('../views/info/info.vue') },
      { path: '/test', component:() => import('../test.vue') },
      {path: '/credit', component: () => import('../views/discover/bycredit.vue')},
      {path: '/genres', component: () => import('../views/discover/bygenres.vue')},
    ]
  })
}