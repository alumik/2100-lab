<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  async mounted () {
    this.$store.commit('menu', sessionStorage.getItem('menu'))
    this.$store.commit('colors', sessionStorage.getItem('colors'))
    let response = await axios.post(
      'http://localhost/api/v1/core/auth/is-authenticated/',
      {
        withCredentials: true
      }
    )
    if (response.data.is_authenticated) {
      this.$store.commit('status')
      try {
        if (response.data.is_staff) {
          let response_two = await axios.get(
            'http://localhost/api/v1/customers/forestage/personal-center/get-customer-detail/'
          )
          this.$store.commit('user', response_two.data)
          this.$store.commit('staff')
          this.$store.commit('groups', response.data.admin_groups)
          this.$store.commit('colors', sessionStorage.getItem('colors'))
          this.$store.commit('menu', sessionStorage.getItem('menu'))
        } else {
          let response_two = await axios.get(
            'http://localhost/api/v1/customers/forestage/personal-center/get-customer-detail/'
          )
          this.$store.commit('user', response_two.data)
          this.$store.commit('staff', false)
          this.$store.commit('colors', sessionStorage.getItem('colors'))
          this.$store.commit('menu', sessionStorage.getItem('menu'))
        }
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
