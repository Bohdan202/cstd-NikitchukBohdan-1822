export default {
  namespaced: true,
  state: {
    items: [
      {
        url: '/home',
        text: 'Home',
        need_auth: false
      },
      // {
      //   url: '/game',
      //   text: 'Game?',
      //   need_auth: true
      // },
      {
        url: '/music',
        text: 'Music',
        need_auth: false
      }
    ]
  },
  getters: {
    items(state, getters, rootState, rootGetters) {
      return state.items.filter(item => {
        return !item.need_auth || (rootGetters.iflogin)
      });
    }
  }
};