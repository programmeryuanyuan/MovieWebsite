<template>
  <div class="app-bg" style="height:auto; min-height: 100%;">
    <navheader></navheader>
    <div class="container">
      <router-view v-slot="{ Component }">
        <component :is="Component"></component>
      </router-view>
    </div>
    <navfooter></navfooter>
    <chatbot></chatbot>
  </div>
</template>
<script>

import navheader from './components/navheader/navheader.vue'
import navfooter from './components/navfooter/navfooter.vue'
//import chatbot from './components/chatbot/chatbot.vue'
import chatbot from './views/chatbot/chatbot.vue'
// import 'bootstrap';

/**
 * 
 */
export default {
  name: 'App',
  components: {
    navheader,
    navfooter,
    chatbot
  },
}
</script>
<style>
@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Sans&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css');

body,
html {
  width: 100%;
  height: 100%;
}

.app-bg {
  display: flex;
  flex-direction: column;
  background-image: url(./assets/bg.jpg);
  height: auto;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  background-attachment: scroll;
  font-family: 'IBM Plex Sans', sans-serif;
}

#app {
  height: 100%;
}

.container {
  width: 1040px;
  margin: 0 auto;
  min-height: calc(100% - 148px);
  height: auto;
}

.v-enter-to,
.v-leave-to {
  position: absolute;
  left: 0;
  right: 0;
}

.animated.faster {
  -webkit-animation-duration: 300ms;
  animation-duration: 300ms;
}
</style>
