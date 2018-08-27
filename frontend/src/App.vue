<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  async created () {
    this.$store.commit('colors', sessionStorage.getItem('colors'))
    this.$store.commit('menu', sessionStorage.getItem('menu'))
    let response = await axios.post(
      'http://localhost:8000/api/v1/core/auth/is-authenticated/',
      {
        withCredentials: true
      }
    )
    if (response.data.is_authenticated) {
      try {
        let res = await axios.get(
          'http://localhost:8000/api/v1/customers/forestage/personal-center/get-customer-detail/'
        )
        this.$store.commit('status')
        this.$store.commit('user', res.data)
      } catch (error) {
        alert(error.message)
      }
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
