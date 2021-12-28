<template>
  <div :class="{'music': true, 'withaudio': this.showplayer, 'withoutaudio': !this.showplayer}" @mouseup="mouseup()">
    <!-- <button @click="play()">play1</button> -->
    <!-- <br> -->

    <MusicDrawer :set_songs="set_songs" />

    <div class="getset stickyup" >
      <input v-model="input_value" class="input" />
      <button @click="getPlaylist()" class="c_button">Get</button>
      <button @click="setPlaylist()" class="c_button">Save</button>
      <button @click="shuffle_playlist()" class="c_button">Shuffle</button>
      <button @click="clear()" class="c_button">Сlear</button>
      <br>

      <div class="line addrectangle">
        <input class="inline addnumber raz" v-model="addnumer" type="number" v-if="!songedit" />
        <input class="inline addsong" v-model="addsong" @keyup.enter="add()" v-if="!songedit" />
        <button class="inline addbutton" @click="add_song()" v-if="!songedit">+</button>

        <input class="inline addnumber raz" v-model="editnumber" type="number" v-if="songedit" />
        <input class="inline addsong" v-model="editsong" @keyup.enter="edit_song()" v-if="songedit" />
        <button class="inline addbutton" @click="edit_song()" v-if="songedit">✓</button>
        <button class="inline addbutton" @click="cancel_edit()" v-if="songedit">X</button>
      </div>
    </div>

    <Loader v-if="isLoading" />

    <ol v-else class="rectangle" @change="updateinstorage()" onselectstart="return false" onmousedown="return false">
      <li v-for="(song, index) in songs" class="line" :key="index" @mousedown="mousedown(index)" @mousemove="songmove(index)">
          <a class="inline song">
            <label class="songname">{{song}}</label>
          </a>
          <div class="play_ico inline" @click="playsong(index)"></div>
          <div class="pencil_ico inline" @click="start_edit(index)"></div>
          <div class="trash_ico inline" @click="deleteSong(index)"></div>
      </li>
    </ol>

  </div>
</template>


<script>

import MusicDrawer from '@/components/MusicDrawer';
import Loader from '@/components/Loader'

// import { mapState } from 'vuex';
import { mapActions, mapGetters, mapMutations } from 'vuex';

export default {
  name: 'Music',
  components: {
    MusicDrawer,
    Loader
  },
  data () {
    return {
      input_value: '',
      songs: [],
      // ...mapState(['songs']),
      selectedsong: null,
      addnumer: '',
      addsong: '',
      editnumber: '',
      startnumber: '',
      editsong: '',
      songedit: false
    }
  },
  watch: {
    songs: function() {
      localStorage.setItem('songs', this.songs.join('@#@'));
      this.setsongs(this.songs);
    },
    input_value: function() {
      localStorage.setItem('playlist', this.input_value);
    }
  },
  methods: {
    ...mapActions(['play']),
    ...mapMutations(['setsongs', 'setplaynumber', 'changeIsLoading']),

    getPlaylist() {
      const value = this.input_value;
      this.changeIsLoading(true);

      if (value.length == 0) return;

      const sended_data = { playlist: value };

      this.$http.post('get_playlist', sended_data)

      .then(response => response.json())
      .then(data => {
        let songs = data.songs;
        this.songs = songs;

        this.changeIsLoading(false)
      })
      .catch((err) => {
        console.log(err)
        this.changeIsLoading(false)
      });

    },
    setPlaylist() {
      const value = this.input_value;
      if (value.length == 0) return;

      const songs = this.songs;

      const sended_data = { 
        playlist: value,
        songs: songs
      };

      this.$http.post('set_playlist', sended_data)

      // .then(response => response.json())
      // .then(data => {
      // })
      .catch((err) => {
        console.log(err)
      });

      // let temp = {};

      // songs.forEach((song, index) => {
      //   temp[index] = song;
      // });

      // // console.log(temp);

      // namesRef.child(value).set(temp);
    },
    add_song() {
      const number = this.addnumer;
      const song = this.addsong;

      if (song) {
        if (number) {
          if (number<1) this.songs.splice(0, 0, song);
          else {
            this.songs.splice(number-1, 0, song);
            this.addnumer = String(Number(number) + 1);
          }
        } else {
          this.songs.push(song);
        }
      }
    },
    edit_song() {
      const startnumber = this.startnumber;
      const number = this.editnumber;
      const song = this.editsong;

      if (song && number) {
        this.songs.splice(startnumber-1, 1);
        this.songs.splice(number-1, 0, song);
      }

      this.songedit = false;
      this.editnumber = '';
      this.editsong = ''
    },
    cancel_edit() {
      this.songedit = false;
      this.editnumber = '';
      this.editsong = ''
    },
    start_edit(index) {
      this.songedit = true;
      this.startnumber = index+1;
      this.editnumber = index+1;
      this.editsong = this.songs[index]
    },
    deleteSong(index) {
      this.songs.splice(index, 1);
    },
    playsong(index) {
      this.setplaynumber(index);
      this.play();
    },
    mousedown(index) {
      this.selectedsong = index;
      // console.log(2, index);
    },
    songmove(index) {
      if (this.selectedsong) {
        let song = this.songs[this.selectedsong];
        // console.log(1, song, this.selectedsong, index);
        this.songs.splice(this.selectedsong, 1);
        this.songs.splice(index, 0, song);
        this.selectedsong = index;
      }
    },
    mouseup() {
      this.selectedsong = null;
    },
    clear() {
      this.songs = [];
      this.input_value = '';
    },
    shuffle_playlist() {
      this.songs.sort(() => Math.random() - 0.5);
    },
    set_songs(songs) {
      this.songs = songs;
    }
  },
  computed: {
    ...mapGetters(['showplayer', 'isLoading'])
  },
  mounted() {
    if (localStorage.getItem('songs')) {
      this.songs = localStorage.getItem('songs').split('@#@');
    }
    if (localStorage.getItem('playlist')) {
      this.input_value = localStorage.getItem('playlist');
    }
    this.changeIsLoading(false);
  }
}
</script>


<style lang="scss" scoped>

h1, h2 {
  font-weight: normal;
}

button {
  cursor: pointer;
}

.music {
  top: 6vh;
  margin: auto;
  max-width: 30rem;
  height: 88vh;
  overflow: auto;
}

.withaudio {
  height: 88vh;
}

.withoutaudio {
  height: 94vh;
}

.addrectangle {
  margin-top: 1rem;
}
.addsong {
  position: relative;
  display: block;
  padding: .4em .4em .4em .8em;
  margin: 0.1rem 0 0.1rem 0.1rem;
  background: #D3D4DA;
  color: #444;
  text-decoration: none;
  -webkit-transition: all .3s ease-out;
  transition: all .3s ease-out;

  margin-left: 0.2em;
  width: 100%;
}
.addnumber {
  // position: absolute;
  // left: 0em;
  // top: 50%;
  // margin-top: -1em;
  background: #9097A2;
  height: 2em;
  width: 2.2em;
  line-height: 2em;
  text-align: center;
  font-weight: bold;

  // display: inline-block;
  margin: auto;
}
.addbutton {
  display: inline-block;
  // position: relative;
  right: 0px;
  height: 1.5rem;
  width: 1.5rem;
  cursor: pointer;
  opacity: .6;
  transition: all .2s;

  margin: auto;
  margin-left: 0.7rem;

  &:hover {
    transform: translateY(-1px);
    // opacity: 1;
  }

  &:active {
    transform: translateY(0px);
  }
}

.raz { 
  -moz-appearance: textfield;
}
.raz::-webkit-inner-spin-button { 
  display: none;
}

.rectangle {
  z-index: 3;
  // margin-top: 1rem;
  counter-reset: li; 
  list-style: none; 
  font: 14px "Trebuchet MS", "Lucida Sans";
  padding: 0;
  text-shadow: 0 1px 0 rgba(255, 255, 255, .5);
}
.rectangle a {
  position: relative;
  display: block;
  padding: .4em .4em .4em .8em;
  margin: 0.1rem 0 0.1rem 0.1rem;
  background: #D3D4DA;
  color: #444;
  text-decoration: none;
  transition: all .3s ease-out;

  margin-left: 2.5em;
  // left: 2.5em;
}
.rectangle a:hover {background: #DCDDE1;}       
.rectangle a:before {
  content: counter(li);
  counter-increment: li;
  position: absolute;
  left: -2.4em;
  // left: 0em;
  top: 50%;
  margin-top: -1em;
  background: #9097A2;
  height: 2em;
  width: 2em;
  line-height: 2em;
  text-align: center;
  font-weight: bold;
}
.rectangle a:after {
  position: absolute;
  content: "";
  border: .5em solid transparent;
  left: -1em;
  top: 50%;
  margin-top: -.5em;
  transition: all .3s ease-out;
}
.rectangle a:hover:after {
  left: -.5em;
  border-left-color: #9097A2;
}

.line {
  display: flex;
  flex-direction: row;
}

.inline {
  display: inline-block;
}

.song {
  width: 100%;
}

.songname {
  overflow: hidden;
}

.pencil_ico, .trash_ico, .play_ico {
  display: inline-block;
  // position: relative;
  right: 0px;
  height: 1.5rem;
  width: 1.5rem;
  cursor: pointer;
  opacity: .6;
  transition: all .2s;

  &:hover {
    transform: translateY(-1px);
    // opacity: 1;
  }

  &:active {
    transform: translateY(0px);
  }
}

.play_ico {
  margin: auto;
  margin-left: 0.7rem;
  background: url('../assets/img/PNG/play.png') no-repeat center;
  background-size: contain;
}

.pencil_ico {
  margin: auto;
  margin-left: 0.7rem;
  background: url('../assets/img/SVG/pencil.svg') no-repeat center;
  background-size: contain;
}

.trash_ico {
  margin: auto;
  margin-left: 0.7rem;
  background: url('../assets/img/SVG/trash.svg') no-repeat center;
  background-size: contain;
}

.getset {
  margin: auto;
  padding-top: 0.5rem;
  background-color: #FFF;
}

.stickyup {
  position: sticky;
  top: 0rem;
  z-index: 5;
} 

.input {
  padding: 0.2rem;
  font-size: 14px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  -moz-box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) inset, 0 2px 10px rgba(0, 0, 0, 0.25);
  -webkit-box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) inset, 0 2px 10px rgba(0, 0, 0, 0.25);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) inset, 0 2px 10px rgba(0, 0, 0, 0.25);
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.5);
  -moz-appearance: none;
  -webkit-appearance: none;
  outline: none;
  color: #333;
}

.c_button {
  appearance: none;
  border: 0;
  border-radius: 2px;
  background: #2c3e50; //#4676D7;
  color: #fff;
  padding: 4px 8px;
  font-size: 14px;
}



// ========================
//       BUTTON THREE
// ========================


.btn-three {
  color: #FFF;
  transition: all 0.5s;
  position: relative;
}

.btn-three::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background-color: rgba(255,255,255,0.1);
  transition: all 0.3s;
}

.btn-three:hover::before {
  opacity: 0 ;
  transform: scale(0.5,0.5);
}

.btn-three::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  opacity: 0;
  transition: all 0.3s;
  border: 1px solid rgba(255,255,255,0.5);
  transform: scale(1.2,1.2);
}

.btn-three:hover::after {
  opacity: 1;
  transform: scale(1,1);
}

</style>
