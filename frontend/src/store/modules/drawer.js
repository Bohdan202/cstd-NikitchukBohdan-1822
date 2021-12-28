export default {
  state: {
    isShowDrawer: false,
  },
  mutations: {
    changeIsShowDrawer(state, payload) {
      state.isShowDrawer = payload;
    }
  },
  actions: {
  },
  getters: {
    isShowDrawer(state) {
      return state.isShowDrawer;
    }
  }
}