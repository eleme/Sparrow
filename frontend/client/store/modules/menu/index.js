import * as types from '../../mutation-types'
import lazyLoading from './lazyLoading'

// show: meta.label -> name
// name: component name
// meta.label: display label

const state = {
  items: [
    {
      name: 'Dashboard',
      path: '/dashboard',
      meta: {
        icon: 'fa-tachometer',
        link: 'dashboard/index.vue'
      },
      component: lazyLoading('dashboard', true)
    },
    {
      name: '项目',
      path: '/project',
      meta: {
        icon: 'fa-list-ul',
        link: 'project/index.vue'
      },
      component: lazyLoading('project', true)
    },
    {
      name: '公共返回模板',
      path: '/template',
      meta: {
        icon: 'fa-copy',
        link: 'template/index.vue'
      },
      component: lazyLoading('template', true)
    },
    {
      name: '收藏',
      path: '/favorite',
      meta: {
        icon: 'fa-heart-o',
        link: 'favorite/index.vue'
      },
      component: lazyLoading('favorite', true)
    }
  ]
}

const mutations = {
  [types.EXPAND_MENU] (state, menuItem) {
    if (menuItem.index > -1) {
      if (state.items[menuItem.index] && state.items[menuItem.index].meta) {
        state.items[menuItem.index].meta.expanded = menuItem.expanded
      }
    } else if (menuItem.item && 'expanded' in menuItem.item.meta) {
      menuItem.item.meta.expanded = menuItem.expanded
    }
  }
}

export default {
  state,
  mutations
}
