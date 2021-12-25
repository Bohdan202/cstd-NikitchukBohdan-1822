import Vue from 'vue';

export default {
  state: {
    nickname: null,
    photo: null
  },
  mutations: {
    setNickname(state, payload) {
      state.nickname = payload;
    },
    setPhoto(state, payload) {
      state.photo = payload;
    }
  },
  actions: {
    getUserData({commit}, end=null) {
      Vue.http.post('get_user_data', {}, { withCredentials: true })
      .then(response => response.json())
      .then(data => {
          console.log(data);
          if (data.status === "ok" && data.user.nickname) {
            commit('setNickname', data.user.nickname);
            commit('setPhoto', data.user.photo);
            // state.nickname = data.user.nickname;
            // state.photo = data.user.photo;
            if (end) end();
          }
          else {
            commit('setNickname', '###notlogin###');
            // state.nickname = " ";
            if (end) end();
          }

      }).catch((err) => {
        state.nickname = '###notlogin###';
        console.log(err)
        
        if (end) end();
      });
    }
    // refresh_token() {
    //   Vue.http.post('refresh_token', {}, { withCredentials: true })
    //   .catch((err) => {
    //     console.log(err)
    //   })
    // }
  },
  getters: {
    nickname(state) {
      return state.nickname;
    },
    photo(state) {
      return state.photo;
    },
    iflogin(state) {
      return state.nickname && state.nickname!=='###notlogin###';
    }
  }
}