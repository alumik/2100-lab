<template>
  <b-navbar
    :sticky="true"
    :toggleable="toggleable"
    type="dark"
    variant="primary"
    class="navbar">
    <button
      id="hide-button"
      class="navbar-toggler"
      @click="$emit('hide')">
      <span
        id="hide-span"
        class="navbar-toggler-icon"/>
    </button>
    <b-navbar-brand
      class="logo">
      <img
        id="logoimg"
        src="../../assets/2100logo.png">
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse"/>
    <b-collapse
      id="nav_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item>{{ $store.state.adminStatus ? '管理员' : '' }}
        </b-nav-item>
        <b-nav-item
          id="logout"
          @click="log">
          {{ $store.state.adminStatus ? '注销' : '登录' }}
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminNavbar',
  data () {
    return {
      toggleable: 'lg'
    }
  },
  methods: {
    log () {
      if (this.$store.state.adminStatus) {
        axios
          .post('http://localhost:8000/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            alert(res.data.message)
            this.$store.commit('adminStatus', false)
            this.$router.push({ path: '/admin' })
          })
          .catch(error => {
            alert(error)
            this.$router.push({ path: '/admin' })
          })
      } else {
        this.$router.push({ path: '/admin' })
      }
    }
  }
}
</script>

<style scoped>
#logout {
  padding-right: 10px;
}

.logo {
  height: 50px;
  margin: 0;
  vertical-align: middle;
}

.logo img {
  height: 35px;
}

.navbar-dark .navbar-nav .nav-link {
  color: #999;
}

.navbar-dark .navbar-nav .nav-link:hover,
.navbar-dark .navbar-nav .nav-link:focus {
  color: #f00;
}

.navbar {
  width: 100vw;
  padding: 10px 5px;
  background-color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  opacity: 0.9;
}

.navbar-toggler {
  margin: 0 15px;
  background-color: #f00;
}
</style>
