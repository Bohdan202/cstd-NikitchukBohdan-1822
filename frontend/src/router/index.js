import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
// import Game from '@/views/Game.vue'
import Music from '@/views/Music.vue'

import store from '../store';

Vue.use(Router)

// const checkAuth = (...[,,next]) => {
//   if (!store.getters.nickname || store.getters.nickname==='###notlogin###') {
//     next({ name: 'Home' })
//     // next('/');
//   }
// }

const router = new Router({
  routes: [
    {
      path: '/',
      redirect: { name: 'Home' }
    },
    {
      name: 'Home',
      path: '/home',
      component: Home,
      meta: { title: 'Home' }
    },
    // {
    //   name: 'Game',
    //   path: '/game',
    //   component: Game,
    //   meta: { title: 'Game', need_auth: true }
    // },
    {
      name: 'Music',
      path: '/music',
      component: Music,
      meta: { title: 'Music' }
    }
  ]
})



router.beforeEach((to, from, next) => {
  store.dispatch('getUserData', () => {
    if (to.meta.need_auth && (!store.getters.iflogin)) {
      next({ name: 'Home' })
    }

    document.title = to.meta.title;
    next()
  });
});

export default router