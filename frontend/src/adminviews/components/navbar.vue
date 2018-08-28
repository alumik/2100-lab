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
        class="logo"
        @click="home">
        <img
          id="logoimg"
          src="../../assets/2100logo.png">
      </b-navbar-brand>
      <div
        class="logout"
        @click="log">
        {{ $store.state.status ? '注销' : '登录' }}
      </div>
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
    home () {
      this.$router.push({ path: '/admin/main' })
    },
    log () {
      if (this.$store.state.status) {
        axios
          .post('http://localhost/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            alert(res.data.message)
            this.$store.commit('status', false)
            this.$store.commit('groups', [])
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
  margin-left: 28px;
  vertical-align: middle;
  cursor: pointer;
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
  user-select: none;
  background-color: #fff !important;
  border-bottom: 1px solid rgba(153, 153, 153, 0.42);
}

.navbar-light .navbar-toggler {
  margin: 0 15px;
  border: none;
  outline: none;
}

.navbar-brand {
  padding: 0;
}

.logout {
  margin-right: 28px;
  color: rgba(0, 0, 0, 0.5);
}

.logout:hover {
  color: #5b9bd1;
}
</style>
