<template>
  <div>
    
    <div class="burger"
      @click="toggleDrawer"
      :class="{'close-drawer': isShowDrawer}">
      <div class="burger__icon" v-show="!isShowDrawer"></div>
      <div class="burger__icon burger__icon--close" v-show="isShowDrawer"></div>
    </div>

    <div class="backdrop" v-if="isShowDrawer" @click="hideDrawer"></div>

    <div class="drawer" :class="{'drawer__hide': !isShowDrawer}">

        <router-link v-for="(item, index) in menuList" :key="index" tag="button"
          :to="item.url" class="list-group-item list-group-item-action" active-class="active">
          <div @click="hideDrawer" class="item_text">{{ item.text }}</div>
        </router-link>

    </div>

  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default {
  name: 'Drawer',
  data() {
    return {

    }
  },
  methods: {
    ...mapMutations(['changeIsShowDrawer']),

    onLogout() {
    },
    toggleDrawer() {
      this.changeIsShowDrawer(!this.isShowDrawer);
    },
    hideDrawer() {
      this.changeIsShowDrawer(false);
    }
  },
  computed: {
    ...mapGetters(['isShowDrawer']),
    ...mapGetters('menu', { menuList: 'items' })
  }
}
</script>

<style lang="scss" scoped>
  $bp-largest: 900px; // 1200px = 75em

  .burger {
    display: none;
    position: fixed;
    top: 1.5vh;
    left: 1.5vw;
    z-index: 9999;
    width: 3rem;
    height: 3vh;
    // outline: 1px solid red;
    cursor: pointer;
    transition: opacity .2s ease-in, left .2s ease-in;
    &:hover {
      opacity: .7;
    }
    &.close-drawer {
      left: 32rem;
    }
    &__icon {
      height: 100%;
      background: url('../assets/img/SVG/burger.svg') no-repeat center;
      background-size: contain;
      &--close {
        background: url('../assets/img/SVG/cross.svg') no-repeat center;
        background-size: contain;
      }
    }
    @media only screen and (max-width: $bp-largest) {
      display: block;
    }
  }

  .backdrop {
    display: none;
    position: fixed;
    z-index: 9991;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: rgba(0,0,0,.7);
    @media only screen and (max-width: $bp-largest) {
      display: block;
    }
  }

  .drawer {
    display: none;
    position: fixed;
    z-index: 9992;
    left: 0;
    top: 0;
    bottom: 0;
    width: 80%;
    max-width: 30rem;
    padding: 2rem 1rem;
    box-sizing: border-box;
    background: #fff;
    transition: transform .2s ease-in;
    box-sizing: border-box;
    &__hide {
      transform: translateX(-30rem);
    }
    .list-group-item {
      display: flex;
      flex-direction: column;
      flex-wrap: wrap;

      width: 100%;

      border: none;
      color: #363d54;
      font-size: 3rem;
      outline: none;
      &.active {
        color: #000;
        background-color: darken(#f8f9fa, 5%);
        margin-top: 0;
      }
    }
    @media only screen and (max-width: $bp-largest) {
      display: block;
    }
  }

  .item_text{
      text-align: center;
      margin-left: auto;
      margin-right: auto;
    }

</style>