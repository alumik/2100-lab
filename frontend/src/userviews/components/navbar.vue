<template>
  <b-navbar
    :sticky="true"
    toggleable="md"
    variant="primary"
    class="my-navbar">
    <button
      id="hamburger"
      class="navbar-toggler"
      @click="$emit('hide')">
      <span class="navbar-toggler-icon"/>
    </button>
    <b-navbar-brand
      class="logo"
      @click="home">
      <img
        id="logoimg"
        src="../../assets/2100logo.png">
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse_user"/>
    <b-collapse
      id="nav_collapse_user"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item
          id="userlogo"
          @click="personal">
          <img
            v-if="$store.state.status"
            id="userimg"
            :src="avatar">{{ $store.state.status ? $store.state.user.username : '' }}
        </b-nav-item>
        <b-nav-item
          id="logout"
          @click="log">
          {{ $store.state.status ? '注销' : '登录' }}
        </b-nav-item>
        <b-alert
          :show="log_test"
          variant="danger"
          dismissible
          @dismissed="log_test=false">
          {{ log_test_error }}
        </b-alert>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserNavbar',
  data () {
    return {
      log_test: false,
      log_test_error: ''
    }
  },
  computed: {
    avatar () {
      return this.$store.state.address + this.$store.state.user.avatar
    }
  },
  mounted () {
    if (this.$store.state.status) {
      axios
        .get(
          'http://localhost/api/v1/customers/forestage/personal-center/' +
            'get-customer-detail/'
        )
        .then(res => {
          this.$store.commit('avatar', res.data.avatar)
        })
        .catch(error => {
          alert(error.message)
        })
    }
  },
  methods: {
    home () {
      this.$router.push({ path: '/' })
    },
    personal () {
      axios
        .post('http://localhost/api/v1/core/auth/is-authenticated/', {
          withCredentials: true
        })
        .then(res => {
          if (res.data.is_authenticated) {
            this.$router.push({ path: '/personal' })
          }
        })
    },
    log () {
      let that = this
      if (that.$store.state.status) {
        axios
          .post('http://localhost/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            alert('您已登出')
            that.$store.commit('status', false)
            that.$router.push({ path: '/' })
          })
          .catch(error => {
            that.log_test = true
            that.log_test_error = error.response.data.message
          })
      } else {
        this.$router.push({ path: '/login' })
      }
    }
  }
}
</script>

<style scoped>
.my-navbar {
  margin: 0;
  vertical-align: middle;
}

#userimg {
  width: 40px;
  height: 40px;
  margin-right: 20px;
  border-radius: 50%;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.logo {
  height: 50px;
  margin-left: 28px;
  vertical-align: middle;
  cursor: pointer;
}

.logo img {
  height: 45px;
}

.nav-link {
  padding: 0;
}

.navbar-dark .navbar-nav .nav-link {
  color: #999;
}

.navbar-dark .navbar-nav .nav-link:hover,
.navbar-dark .navbar-nav .nav-link:focus {
  color: lightgray;
}

.navbar {
  padding: 10px 5px;
  background-color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  opacity: 0.8;
}

.navbar-toggler {
  background-color: lightgray;
}

#userimg:hover {
  -webkit-filter: brightness(150%);
  filter: brightness(150%);
}

#logoimg:hover {
  -webkit-filter: brightness(150%);
  filter: brightness(150%);
}

#logout {
  padding: 6px;
}

.navbar-light .navbar-toggler {
  margin: 0 15px;
  border: none;
  outline: none;
}
</style>
