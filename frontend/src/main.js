import './assets/scss/styles.scss'

import Vue from 'vue';
import App from './App';
import router from './router';
import store from './store';

import './firebase';

import VueResource from 'vue-resource';
import VueCookies from 'vue-cookies';
// import VueYoutube from 'vue-youtube';
import { firestorePlugin } from 'vuefire';

Vue.config.productionTip = false


Vue.use(VueResource);
Vue.use(VueCookies);
// Vue.use(VueYoutube)
Vue.use(firestorePlugin);

// Vue.http.options.root = '';
// Vue.http.options.root = 'http://localhost:5555/';
// Vue.http.options.root = 'https://app-72.herokuapp.com/';

if (process.env.NODE_ENV === 'development') Vue.http.options.root = 'http://192.168.0.129:5000/';
else Vue.http.options.root = window.location.origin + '/';

console.log(Vue.http.options.root);

// import VueSocketIO from 'vue-socket.io'
 
// Vue.use(new VueSocketIO({
//     debug: false,
//     connection: Vue.http.options.root,
// }))

// Pusher.logToConsole = true;

Vue.use(require('vue-pusher'), {
    api_key: '11a3c34b3c5456540148',
    options: {
      cluster: 'eu',
      // encrypted: true,
    }
});

new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
