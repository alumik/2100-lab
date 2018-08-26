<template>
  <b-navbar
    id="user-navbar"
    :sticky="true"
    toggleable="md"
    type="dark"
    variant="primary"
    class="my-navbar">
    <button
      id="hamburger"
      class="navbar-toggler"
      @click="$emit('hide')">
      <span class="navbar-toggler-icon"/>
    </button>
    <b-navbar-brand
      id="logo"
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
    }
  },
  computed: {
    avatar () {
      return this.$store.state.address + this.$store.state.user.avatar
    }
  },
  created () {
    // let that = this
    // axios
    //   .post('http://localhost:8000/api/v1/core/auth/is-authenticated/')
    //   .then(res => {
    //     // console.log('登录状态：' + res.data.is_authenticated)
    //     if (res.data.is_authenticated) {
    //       that.$store.commit('status')
    //       // console.log(that.$store.state)
    //     }
    //   })
  },
  mounted () {},
  methods: {
    home () {
      this.$router.push({ path: '/' })
    },
    personal () {
      axios
        .post('http://localhost:8000/api/v1/core/auth/is-authenticated/', {
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
          .post('http://localhost:8000/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            // console.log(res.data.message)
            alert('您已登出')
            that.$store.commit('status', false)
            that.$router.push({ path: '/' })
          })
        //   .catch(error => {
        //  console.log(error.message)
        // })
      } else {
        this.$router.push({ path: '/login' })
      }
    }
  }
}
</script>

<style>
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
  margin: 0;
  vertical-align: middle;
}

.logo img {
  height: 35px;
}

.nav-link {
  padding: 0;
}

.navbar-dark .navbar-nav .nav-link {
  color: #999;
}

.navbar-dark .navbar-nav .nav-link:hover,
.navbar-dark .navbar-nav .nav-link:focus {
  color: #f00;
}

.navbar {
  padding: 10px 5px;
  background-color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  opacity: 0.8;
}

.navbar-toggler {
  background-color: #f00;
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
</style>
