export default {
  state: {
    isLoading: false,
    isDownloading: false
  },
  mutations: {
    changeIsLoading(state, payload) {
      state.isLoading = payload;
    },
    changeIsDownloading(state, payload) {
      state.isDownloading = payload;
    }
  },
  getters: {
    isLoading(state) {
      return state.isLoading;
    },
    isDownloading(state) {
      return state.isDownloading;
    }
  }
}