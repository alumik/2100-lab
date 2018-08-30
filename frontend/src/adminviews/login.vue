<template>
  <div>
    <b-navbar
      :sticky="true"
      toggleable="md"
      type="dark"
      variant="primary"
      class="navbar">
      <b-navbar-brand
        class="logo">
        <img
          id="logoimg"
          src="../assets/2100logo.png">
      </b-navbar-brand>
      <b-navbar-toggle target="nav_collapse"/>
      <b-collapse
        id="nav_collapse"
        is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item
            id="logout"
            @click="log">
            {{ $store.state.status ? '注销' : '登录' }}
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div class="container">
      <h2 class="my-head-first">2100实验室</h2>
      <h2 class="my-head-second">后台登录入口</h2>
      <br>
      <form>
        <b-input-group prepend="手机号">
          <b-form-input
            v-model="phone_number"
            type="text"/>
        </b-input-group>
        <br>
        <b-input-group prepend="密码">
          <b-form-input
            v-model="password"
            type="password"/>
          <b-input-group-append/>
        </b-input-group>
        <b-button
          id="btn"
          :disabled="disabled"
          type="submit"
          variant="outline-success"
          @click="check">
          登录
        </b-button>
        <br>
        <p>{{ error_message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'AdminLogin',
  data: function () {
    return {
      phone_number: '',
      password: '',
      error_message: '',
      disabled: false
    }
  },
  methods: {
    check (evt) {
      this.disabled = true
      const regix = /^1\d{10}$/
      let result = this.phone_number.match(regix)
      if (result === null) {
        this.error_message = '请输入一个正确的手机号！'
        this.disabled = false
      } else {
        this.error_message = ''
        axios
          .post(
            'http://localhost/api/v1/admin/backstage/auth/authenticate-admin/',
            qs.stringify({
              phone_number: this.phone_number,
              password: this.password
            })
          )
          .then(response => {
            this.$store.commit('status')
            this.$store.commit('staff')
            this.$store.commit('username', response.data.username)
            this.$router.push({ path: '/admin/main' })
          })
          .catch(error => {
            this.disabled = false
            let errorMessage = error.response.data.message
            if (errorMessage === 'User is already authenticated.') {
              this.error_message = '用户已登录'
            } else if (errorMessage === 'Invalid phone number or password.') {
              this.error_message = '用户输入密码错误，请重新输入'
            } else if (errorMessage === 'Access denied.') {
              this.error_message = '该用户不是管理员'
            } else {
              this.error_message = '数据库错误'
            }
          })
      }
      evt.preventDefault()
    },
    log () {
      let that = this
      if (that.$store.state.status) {
        axios
          .post('http://localhost/api/v1/core/auth/logout/', {
            withCredentials: true
          })
          .then(res => {
            alert(res.data.message)
            that.$store.commit('status', false)
            that.$router.push({ path: '/admin' })
          })
          .catch(error => {
            alert(error.message)
          })
      } else {
        this.$router.push({ path: '/admin' })
      }
    }
  },
  async beforeRouteEnter (to, from, next) {
    let response = await axios.post(
      'http://localhost/api/v1/core/auth/is-authenticated/',
      {
        withCredentials: true
      }
    )
    if (response.data.is_authenticated && response.data.is_staff) {
      next('/admin/main')
    } else if (response.data.is_authenticated && !response.data.is_staff) {
      next('/')
    } else {
      next()
    }
  }
}
</script>

<style scoped>
#logout {
  padding-right: 35px;
}

.logo {
  height: 50px;
  margin-left: 35px;
  vertical-align: middle;
}

.logo img {
  height: 35px;
}

.navbar-dark .navbar-nav .nav-link {
  color: #999;
}

.my-head-first {
  margin-top: 20%;
  margin-bottom: 5%;
}

.my-head-second {
  margin-bottom: 30%;
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

.container {
  display: block;
  width: 350px;
  height: 500px;
  margin: 100px auto;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 5px 6px 5px rgba(0, 0, 0, 0.1);
}

#btn {
  margin-top: 40px;
  margin-bottom: 20px;
}

.input-group-text {
  min-width: 70px;
  max-width: 70px;
}
</style>
