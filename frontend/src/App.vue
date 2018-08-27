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
    this.$store.commit('colors', sessionStorage.getItem('colors'))
    this.$store.commit('menu', sessionStorage.getItem('menu'))
    let response = await axios.post(
      'http://localhost:8000/api/v1/core/auth/is-authenticated/',
      {
        withCredentials: true
      }
    )
    if (response.data.is_authenticated) {
      this.$store.commit('status')
      try {
        if (response.data.is_staff) {
          let res = await axios.get(
            'http://localhost:8000/api/v1/customers/forestage/personal-center/get-customer-detail/'
          )
          this.$store.commit('user', res.data)
          res = await axios.get(
            'http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/',
            {
              params: {
                admin_id: response.data.user_id
              }
            }
          )
          this.$store.commit('groups', res.data.admin_groups)
          // console.log(this.$store.state.user)
          // for (let permission of res.data.admin_groups) {
          // }
          this.$store.commit('menu', sessionStorage.getItem('menu'))
        } else {
          let res = await axios.get(
            'http://localhost:8000/api/v1/customers/forestage/personal-center/get-customer-detail/'
          )
          this.$store.commit('user', res.data)
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
