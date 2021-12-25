<template>
  <div>

    <Loader v-if="isLoading" />
    <div v-else>
      <h2>under development</h2>
      <!-- <input v-model="value" /> -->
      <!-- <button @click="test">button</button> -->
    </div>
    
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import Loader from '@/components/Loader';

export default {
  name: 'Home',
  components: { Loader },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      value: ''
    }
  },
  methods: {
    ...mapMutations(['changeIsLoading']),
    getData() {
      this.changeIsLoading(true);

      const sended_data = {};

      const url = 'test';
      this.$http.post(url, sended_data)

      .then(response => { return response.json(); })
      .then(data => {
        this.changeIsLoading(false);
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // test() {
    //   this.$http.post('test_pusher', {})

    //   .then(response => { return response.json(); })
    //   .then(data => {
    //     console.log('ok');
    //   })
    //   .catch((err) => {
    //     console.log(err)
    //   })
    // }
  },
  computed: {
    ...mapGetters(['isLoading']),
  },
  mounted() {
    // this.getData();
    
    // this.$pusher.subscribe('mychannel').bind('myevent', function(data) {
    //   console.log(data.message);
    // });
  }
}
</script>

<style lang="scss" scoped>

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

</style>
