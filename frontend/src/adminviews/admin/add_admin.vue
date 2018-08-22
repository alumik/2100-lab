<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>新增管理员</h2>
      {{ error_message }}
      <div>
        <div class="form-group">
          <label
            class="form-check-label"
            for="telephone">管理员手机号</label>
          <input
            id="telephone"
            v-model="admin.phone_number"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group">
          <label
            class="form form-check-label"
            for="password">管理员密码</label>
          <input
            id="password"
            v-model="admin.password"
            class="form-control col-lg-3"
            type="password">
        </div>
        <div class="form-group">
          <label
            class="form form-check-label"
            for="passwordagain">再次输入密码</label>
          <input
            id="passwordagain"
            v-model="admin.password_again"
            class="form-control col-lg-3"
            type="password">
        </div>
        <button
          class="btn btn-sm"
          @click="checkFormat"
        >保存</button>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'AddAdmin',
  components: {Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '新增管理员',
        active: true
      }],
      admin: {
        phone_number: null,
        password: null,
        password_again: null
      },
      error_message: ''
    }
  },
  methods: {
    checkFormat: function () {
      this.error_message = ''
      if (this.admin.phone_number === null) {
        this.error_message = '请输入手机号！'
        return
      }
      const regix = /^1\d{10}$/
      let result = this.admin.phone_number.match(regix)
      if (result === null) {
        this.error_message = '请输入一个正确的手机号！'
      } else if (this.admin.password === null) {
        this.error_message = '请输入密码！'
      } else if (this.admin.password_again === null) {
        this.error_message = '请再次输入密码！'
      } else if (this.admin.password !== this.admin.password_again) {
        this.error_message = '两次输入密码不相符，请重新输入！'
      } else {
        this.sendMessage()
      }
    },
    sendMessage: function () {
      let _this = this
      axios.post('http://localhost:8000/api/v1/admin/backstage/admin-management/add-admin/', qs.stringify({
        phone_number: this.admin.phone_number,
        password: this.admin.password
      })).then(
        response => {
          if (response.data.new_admin_id) {
            _this.error_message = '添加成功'
            _this.admin.phone_number = ''
            _this.admin.password = ''
            _this.admin.password_again = ''
            // this.$router.push({name: 'AdminManagement'})
          }
        }
      ).catch(
        error => {
          _this.error_message = error.response.message
        }
      )
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .form-group {
    margin-top: 25px;
  }

  .btn {
    margin-top: 25px;
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .btn:active {
    background-color: #5e0057;
  }
</style>
