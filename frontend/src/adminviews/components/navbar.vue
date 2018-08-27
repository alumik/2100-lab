<template>
  <b-navbar
    :sticky="true"
    :toggleable="toggleable"
    type="light"
    variant="primary"
    class="navbar">
    <div class="container-fluid">
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
          <b-nav-item>{{ $store.state.status ? $store.state.user.username : '' }}
          </b-nav-item>
          <b-nav-item
            @click="log">
            {{ $store.state.status ? '注销' : '登录' }}
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </div>
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
      if (this.$store.state.status) {
        axios
          .post('http://localhost:8000/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            alert(res.data.message)
            this.$store.commit('status', false)
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
.logo {
  height: 50px;
  margin-left: 30px;
  vertical-align: middle;
}

.logo img {
  height: 45px;
}

.navbar-light .navbar-nav .nav-link {
  color: #999;
}

.navbar-light .navbar-nav .nav-link:hover,
.navbar-light .navbar-nav .nav-link:focus {
  color: #5b9bd1;
}

.navbar {
  padding: 10px 5px;
  background-color: #fff !important;
  border-bottom: 1px solid rgba(153, 153, 153, 0.42);
}

.navbar-light .navbar-toggler {
  margin: 0 15px;
  border: none;
  outline: none;
}
</style>
