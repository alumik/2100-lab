<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  destroyed () {
    if (this.$store.state.status) {
      axios
        .post('http://localhost:8000/api/v1/core/auth/logout/', {
          withCredentials: true
        })
        .then(res => {
          this.$store.commit('status', false)
        })
        .catch(error => {
          alert(error)
        })
    }
  }
}
</script>

<style>
html,
body {
  height: 100%;
}

#app {
  height: 100%;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  text-align: center;
}
</style>
