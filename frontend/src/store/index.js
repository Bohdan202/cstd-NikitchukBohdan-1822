import Vue from 'vue';
import Vuex from 'vuex';

import menu from './modules/menu';
import drawer from './modules/drawer';
import loader from './modules/loader';
import audioplayer from './modules/audioplayer';
import user from './modules/user';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    menu,
    drawer,
    loader,
    audioplayer,
    user
  },
  // strict: process.env.NODE_ENV !== 'production'
})
