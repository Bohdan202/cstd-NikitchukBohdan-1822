<template>
  <div>
    <div class="button" @click="toggleDrawer">
      <p class="inbutton">more ⯅</p>
    </div>

    <div id="mySidenav" :class="{
      sidenav: true,
      sidenav_show: isShow,
      sidenav_hide: !isShow
    }">
      <div class="closebtn" @click="hideDrawer()">&times;</div>
      
      <div class="getset" v-if="isShow">
        <p class="ptitle">Spotify <button class="helpbutton" @click="shelp()">?</button></p>
        <input type="text" v-model="input_svalue" class="input" />
        <button @click="getSpotyfyPlaylist()" class="getbutton">Get</button>
      </div>
      <br>
      <div class="getset" v-if="isShow">
        <p class="ptitle">VK <button class="helpbutton" @click="vkhelp()">?</button></p>
        <input type="text" v-model="input_vkvalue" class="input" />
        <button @click="getVkPlaylist()" class="getbutton">Get</button>
      </div>


    </div>

  </div>
</template>

<script>

export default {
  name: 'DiscordBotDrawer',
  data() {
    return {
      input_svalue: '',
      input_vkvalue: '',
      isShow: false,
    }
  },
}
</script>

<style lang="scss" scoped>
$bp-largest: 900px; // 1200px = 75em

input[type=text] {
    width: 80%;
    padding: 0.3rem 0.5rem;
    margin: 0.2rem 0;
    box-sizing: border-box;
    border: 3px solid #ccc;
    -webkit-transition: 0.5s;
    transition: 0.5s;
    outline: none;
}

input[type=text]:focus {
    border: 3px solid #555;
}

.getbutton {
  padding: 0.3rem 0.5rem;
}

.ptitle {
  width: 100%;
  color: #fff;
  text-align: center;

  padding: 0.4rem 0.5rem;
}

.helpbutton {
  width: 1.2rem;
  height: 1.2rem;
  background-color: #000;
  color: #fff;
}

.button {
  width: 2rem;
  height: 7rem;

  padding: 1.5rem 0rem 1rem 0rem;

  position: fixed;
  right: 0;
  background-color: #151515;

  top: 50%;

  z-index: 1;
}

.inbutton {
  color: #fff;

  text-align: center;
  vertical-align: middle;

  transform: rotate(-90deg);

  width: 4rem;
  height: 4rem;
}

.sidenav_show {
  min-width: 20rem;
  max-width: 45rem;
}

.sidenav_hide {
 max-width: 0.2rem;
}

.sidenav {
  height: 100%;
  position: fixed;
  z-index: 1;
  top: 6vh;
  right: 0;
  background-color: #111;
  overflow-x: hidden; // Disable horizontal scroll
  padding-top: 55px;
  transition: 0.8s;

  padding-left: 0.2rem;
  z-index: 8;
}

// The navigation menu links
.sidenav a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

// /When you mouse over the navigation links, change their color
.sidenav a:hover {
  color: #f1f1f1;
}

// Position and style the close button (top right corner)
.sidenav .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
  z-index: 5;
}

// Style page content - use this if you want to push the page content to the right when you open the side navigation
#main {
  transition: margin-left .5s;
  padding: 20px;
}

// On smaller screens, where height is less than 450px, change the style of the sidenav (less padding and a smaller font size)
@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}

</style>