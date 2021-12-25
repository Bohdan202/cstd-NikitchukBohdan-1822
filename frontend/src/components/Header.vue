<template>
  <div>
    <div class="headerinside" onselectstart="return false" onmousedown="return false">
      <font color="black">
        <nav>
          <ul>
            <img src="..\assets\logo.png" alt="logo" class="logo_img">
            <!-- <li class="logo">Project_72</li> -->
            <li class="logo"></li>

            <router-link v-for="(item, index) in menuList" :key="index" tag="li"
              :to="item.url" class="items" active-class="active">
              <a>{{ item.text }}</a>
            </router-link>

            <li class="btn">
              <a href="#"><i class="fas fa-bars"></i></a>
            </li>
          </ul>

          <img :src="photo" alt="" class="mainphoto" @click="showMenu=!showMenu" v-if="iflogin">
          <ul :class="{ usermenu: true, submenu: !showMenu, topmenu: showMenu }">
            <li><a class="nickname">{{nickname}}</a></li>
            <li><a>Item 1</a></li>
            <li><a>Item 2</a></li>
            <li><a @click="logout()">Log out</a></li>
          </ul>
          <div class="googlelogin" @click="glogin()" v-if="nickname && nickname==='###notlogin###'" />
        </nav>
      </font>
    </div>
  </div>
</template>


<script>

import { mapActions, mapGetters } from 'vuex';
import { googleLogin, ifgoogleLogin } from '@/firebase';

export default {
  name: "Header",
  data() {
    return {
      msg: "",
      showMenu: false
    };
  },
  computed: {
    ...mapGetters('menu', { menuList: 'items' }),
    ...mapGetters(['nickname', 'iflogin', 'photo'])
  },
  methods: {
    ...mapActions(['getUserData']),
    glogin() {
      googleLogin();
      // googleLogin(this.$http, this.$cookies, this.getUserData);
    },
    logout() {
      this.$cookies.remove('uid')
      this.$cookies.remove('token')
      this.getUserData();
      this.showMenu = false;
    }
  },
  beforeMount() {
    ifgoogleLogin(this.$http, this.$cookies, this.getUserData)
    // this.getUserData();
  },
  mounted() {
  }
};

</script>


<style lang="scss">
$bp-largest: 900px; // 1200px = 75em

.mainphoto {
  position: fixed;
  right: 1rem;
  top: 0.5rem;

  height: 2rem;
  width: 2rem;

  border-radius: 100px;
  border: 2px solid rgb(128, 128, 128);
  box-shadow: 0 0 7px #666;

  cursor: pointer;
}

.headerinside {
  height: 100%;
  background: #151515;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}

.logo_img {
  left: 1.5rem;
  top: 0.5rem;
  
  height: 2rem;
  
  position: fixed;
}

nav {
  background: #151515;
  padding: 0.5rem 4rem;

  padding-top: 0.8rem;
  padding-right: 20vw;
}

nav ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;

  @media only screen and (max-width: $bp-largest) {
    display: none;
  }
}

nav ul li {
  // padding: 1rem 0;
  cursor: pointer;
}

nav ul li.items {
  position: relative;
  width: auto;
  margin: 0 1.2rem;
  text-align: center;
  order: 3;
}

// nav ul li.items:after {
//   position: absolute;
//   content: '';
//   left: 0;
//   bottom: 0.5rem;
//   height: 0.2rem;
//   width: 100%;
//   background: #33ffff;
//   opacity: 0;
//   transition: all 0.2s linear;
// }

nav ul li.items:hover:after {
  opacity: 1;
  bottom: 0.8rem;
}

nav ul li.logo {
  flex: 1;
  color: white;
  font-size: 2rem;
  font-weight: 600;
  cursor: default;
  user-select: none;
}

nav ul li a {
  color: white;
  font-size: 18px;
  text-decoration: none;
  transition: .4s;
}

nav ul li:hover a {
  color: cyan;
}

nav ul li i {
  font-size: 20px;
}

nav ul li.btn {
  display: none;
}
nav ul li.btn.hide i:before {
  content: '\f00d';
}
@media all and (max-width: 900px) {
  nav{
    padding: 0.5rem 2rem;
  }
  nav ul li.items {
    width: 100%;
    display: none;
  }
  nav ul li.items.show {
    display: block;
  }
  nav ul li.btn {
    display: block;
  }
  nav ul li.items:hover {
    border-radius: 5px;
    box-shadow: inset 0 0 5px #33ffff,
                inset 0 0 10px #66ffff;
  }
  nav ul li.items:hover:after {
    opacity: 0;
  }
}

.googlelogin {
  margin: auto;
  margin-left: 0.7rem;
  background: url('../assets/img/PNG/btn_google_signin_dark_normal_web.png') no-repeat center;
  background-size: contain;

  position: fixed;
  right: 0.5rem;
  top: 0.5rem;

  height: 2rem;
  width: 10rem;

  cursor: pointer;

  // border-radius: 100px;
  // border: 2px solid rgb(128, 128, 128);
  // box-shadow: 0 0 7px #666;
}

.submenu { display: none; }
.topmenu { display: block; }
.usermenu {
  position: fixed;
  right: 0;
  top: 3rem;

  background: #151515;

  .nickname {
    border: 0;
  }

  li {
    border: 1px solid rgba(255, 255, 255, 0.5);
    padding-left: 10px;
  }

  a {
    display: block;
    padding: 10px 15px;
    text-decoration: none;
    outline: none;
    font-family: 'Lora', serif;
    transition: .5s linear;
  }
}
</style>
