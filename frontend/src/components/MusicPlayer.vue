<template>
  <div>
    <div class="show_button" v-if="!isShow" @click="toggleDrawer()">
      ▲
    </div>
    <div class="hide_button" v-if="isShow" @click="toggleDrawer()">
      ▼
    </div>

    <div class="container-audio" v-show="isShow">
      <audio controls id="audio"
      @volumechange="volumechange()"
      @ended="ended()"
      @canplay="canplay()"
      >
        <!-- <source :src="song" type="audio/mpeg"> -->
        <!-- <source v-bind:src="song" type="audio/ogg"> -->
        <!-- <source src="https://r1---sn-05goxu-3c2s.googlevideo.com/videoplayback?expire=1619754456&ei=eCmLYNfxCo-V1gLG-of4Ag&ip=194.44.216.254&id=o-AN2ds5k5DZiiB_XTGHOoX2zpXdCDEQBzN6tYmXd93hxf&itag=249&source=youtube&requiressl=yes&mh=mo&mm=31%2C29&mn=sn-05goxu-3c2s%2Csn-3c27snel&ms=au%2Crdu&mv=m&mvi=1&pl=24&initcwndbps=1253750&vprv=1&mime=audio%2Fwebm&ns=Nqk9FbuaBAqOMmQH28rd1ToF&gir=yes&clen=1392346&dur=207.261&lmt=1608504936416820&mt=1619732208&fvip=1&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=5431432&n=zNtwO-8GVNXNy28&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgTdbB-FwQFhZKb4KNk6A5nEDW2_jqGYjdxyJRxlPvQYkCIBxwHhKaq9AzGXq6mnJy4tt7JdrRzkmU0k9Ueauzj6aj&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhALqBtCON2KOF73_QnSPO5DxPtlRcCQbD49X-N6jZfxcPAiA71TumAOyAqzemXLQoBPTwzTXJy4r00r62q7SSP2kn-A%3D%3D" type="audio/ogg"> -->
        Your browser dose not Support the audio Tag
      </audio>
    </div>
  </div>
</template>

<script>

import { mapActions, mapGetters, mapMutations } from 'vuex';

export default {
  name: 'MusicPlayer',
  data() {
    return {
      isShow: true,
      volume: 0.5,
    }
  },
  watch: {
    volume: function() {
      localStorage.setItem('volume', this.volume);
    },
    isShow: function() {
      localStorage.setItem('isShow', this.isShow && 1 || 0);
      this.setisShow(this.isShow);
    },
  },
  methods: {
    ...mapActions(['play']),
    ...mapMutations(['setplaynumber', 'setisShow']),

    toggleDrawer() {
      this.isShow = !this.isShow;
      // this.isShow = true;
    },
    hideDrawer() {
      this.isShow = false;
    },

    volumechange() {
      this.volume = this.audio.volume;
    },
    ended() {
      try {
        this.setplaynumber(this.playnumber+1);
        this.play();
      } catch(err) {
        console.log("error in audioplayer");
      };
    },
    loadaudio() {
      try {
        this.play({end: () => {this.audio.pause()}});
      } catch(err) {
        console.log("error in audioplayer");
      };
    },
    canplay() {
      this.audio.volume = this.volume;
    }

  },
  computed: {
    ...mapGetters(['songs', 'playnumber']),
    audio() {
      try {
        return document.getElementById("audio");
      } catch (err) { console.log(err) }
    }
  },
  mounted() {
    if (localStorage.getItem('volume')) {
      this.volume = localStorage.getItem('volume');
    }
    if (localStorage.getItem('isShow')) {
      this.isShow = Boolean(Number(localStorage.getItem('isShow')));
    }

    this.loadaudio();

  }
}
</script>

<style lang="scss" scoped>
$bp-largest: 900px; // 1200px = 75em

.show_button {
  bottom: 0vh;
}

.hide_button {
  bottom: 6vh;
}

.show_button, .hide_button {
  width: 3vh;
  height: 2vh;
  font-size: 2vh;
  position: fixed;

  right: 4vw;

  border: 1px solid #444;
  border-radius: 7px 7px 0 0;

  text-align: center;

  z-index: 15;

  cursor: pointer;
}

// Global Reset
* {
    font-family: 'Allerta', arial, Tahoma;
    box-sizing: border-box;
}

h3 {
  text-shadow: 1px 1px 1px #fff;
}

.container-audio {
  position: fixed;
  width: 100vw;
  height: 6vh;
  left: 0;
  bottom: 0;
  border: 1px solid #444;
  background-color: #eee;
  color: #444;
  overflow: hidden;

  z-index: 15;
}
audio {
  width: 100%;
}
audio:nth-child(2), audio:nth-child(4), audio:nth-child(6) {
    margin: 0;
}
.container-audio, .colum1 {
  width: 23px;
  border-radius: 5px;
  display: inline-block;
  position: relative;
}
.container-audio, .colum1:last-child {
  margin: 0;
}
.container-audio, .colum1, .row {
  width: 100%;
  border-radius: 5px;
  position: absolute;
  -webkit-animation: Rofa 10s infinite ease-in-out;
  animation: Rofa 10s infinite ease-in-out;
  bottom: 0;
}


</style>