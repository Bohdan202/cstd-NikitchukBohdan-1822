<template>
  <div id="app">
    <Header class="header stickyup" />
    <router-view class="body"/>

    <Drawer />
    <MusicPlayer />
    <Chat />
  </div>
</template>

<script>
  import Header from './components/Header';
  import Drawer from './components/Drawer';
  import MusicPlayer from '@/components/MusicPlayer';
  import Chat from '@/components/Chat';

  export default {
    name: 'App',
    components: {
      Header,
      Drawer,
      MusicPlayer,
      Chat
    }
  }
</script>

<style scoped lang="scss">
  $bp-largest: 75em; // 1200px = 75em
  $bp-large: 56.25em; // 900px = 56.25em
  $bp-medium: 45em; // 720px = 45em
  $bp-small: 37.5em; // 600px = 37.5em
  $bp-smallest: 25em; // 400px = 25em

  // .body {
  //   background-color: #f1f1f1;
  // }

  .stickyup {
    // position: sticky;
    top: 0;
    z-index: 10;
  } 

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    // text-align: center;
    color: #2c3e50;
    margin: 0;
  }

  .header {
    height: 3rem;
    z-index: 10;
  }

  // .body {
  //   height: 94vh;
  //   // width: 98vw;
  // }

</style>
