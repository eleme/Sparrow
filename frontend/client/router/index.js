import Vue from 'vue'
import Router from 'vue-router'
import menuModule from 'vuex-store/modules/menu'
Vue.use(Router)

export default new Router({
  mode: 'hash', // Demo is living in GitHub.io, so required!
  linkActiveClass: 'is-active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      name: '403',
      path: '/403',
      component: require('../views/403')
    },
    {
      name: 'Home',
      path: '/',
      component: require('../views/Home')
    },
    {
      name: '登录',
      path: '/login',
      component: require('../views/auth/Login')
    },
    {
      name: '项目 / 添加',
      path: '/project/create',
      component: require('../views/project/create')
    },
    {
      name: '项目 / API',
      path: '/project/detail/:id',
      component: require('../views/project/detail')
    },
    {
      name: '项目 / API / 添加',
      path: '/project/:project_id/api/create',
      component: require('../views/api/create')
    },
    {
      name: '项目 / API / 更新',
      path: '/project/:project_id/api/update/:api_id',
      component: require('../views/api/update')
    },
    {
      name: '项目 / API / 详情',
      path: '/project/:project_id/api/detail/:api_id',
      component: require('../views/api/detail')
    },
    {
      name: '公共模板 / 添加',
      path: '/template/create',
      component: require('../views/template/create')
    },
    {
      name: '公共模板 / 详情',
      path: '/template/detail/:id',
      component: require('../views/template/detail')
    },
    {
      name: '公共模板 / 更新',
      path: '/template/update/:id',
      component: require('../views/template/update')
    },
    ...generateRoutesFromMenu(menuModule.state.items),
    {
      path: '*',
      redirect: '/'
    }
  ]
})

// Menu should have 2 levels.
function generateRoutesFromMenu (menu = [], routes = []) {
  for (let i = 0, l = menu.length; i < l; i++) {
    let item = menu[i]
    if (item.path) {
      routes.push(item)
    }
    if (!item.component) {
      generateRoutesFromMenu(item.children, routes)
    }
  }
  return routes
}
