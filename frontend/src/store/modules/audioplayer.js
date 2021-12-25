import Vue from 'vue';

export default {
    state: {
        songs: localStorage.getItem('songs') && localStorage.getItem('songs').split('@#@') || [],
        playnumber: localStorage.getItem('playnumber') && Number(localStorage.getItem('playnumber')) || 0,
        isShow: true
    },
    mutations: {
        setsongs(state, payload) {
            state.songs = payload;
        },
        setplaynumber(state, payload) {
            state.playnumber = payload;
            localStorage.setItem('playnumber', payload);
        },
        setisShow(state, payload) {
            state.isShow = payload;
        }
    },
    actions: {
        play({state}, arg=null) {
            let index = state.playnumber;
            let name = state.songs[index];
            const sended_data = { name: name };
      
            Vue.http.post('get_source', sended_data)
            .then(response => response.json())
            .then(data => {
                // console.log(data);

                let audio = document.getElementById("audio");
                audio.src = data.source;

                try {
                    audio.play();
                    if (arg) arg.end();
                } catch(err) {
                    console.log("error in audioplayer");
                };

            }).catch((err) => {
                console.log(err)
            });
        },
    },
    getters: {
        songs(state) {
            return state.songs;
        },
        playnumber(state) {
            return state.playnumber;
        },
        showplayer(state) {
            return state.isShow;
        },
    }
  }