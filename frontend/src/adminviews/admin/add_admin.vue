<template>
  <Basic :items="items">
    <div class="my-content">
      <h1>新增管理员</h1>
      <Alert
        :count_down="wrong_count_down"
        :instruction="error_message"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <Alert
        :count_down="success_count_down"
        :instruction="error_message"
        variant="success"
        @decrease="success_count_down-1"
        @zero="success_count_down=0"/>
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
        <a
          id="save-btn"
          class="btn"
          @click="check_format">
          <simple-line-icons
            id="add-icon"
            icon="pin"
            color="white"
            class="icon"/>
          保存
        </a>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'AddAdmin',
  components: { Alert, Basic },
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '管理员管理',
          href: '/admin/adminmanagement'
        },
        {
          text: '新增管理员',
          active: true
        }
      ],
      admin: {
        phone_number: null,
        password: null,
        password_again: null
      },
      wrong_count_down: 0,
      success_count_down: 0,
      error_message: ''
    }
  },
  methods: {
    check_format: function () {
      this.error_message = ''
      if (this.admin.phone_number === null) {
        this.error_message = '请输入手机号'
        this.wrong_count_down = 5
        return
      }
      const regix = /^1\d{10}$/
      let result = this.admin.phone_number.match(regix)
      if (result === null) {
        this.error_message = '请输入一个正确的手机号'
        this.wrong_count_down = 5
      } else if (this.admin.password === null) {
        this.error_message = '请输入密码'
        this.wrong_count_down = 5
      } else if (this.admin.password_again === null) {
        this.error_message = '请再次输入密码'
        this.wrong_count_down = 5
      } else if (this.admin.password !== this.admin.password_again) {
        this.error_message = '两次输入密码不相符，请重新输入'
        this.wrong_count_down = 5
      } else {
        this.send_message()
      }
    },
    send_message: function () {
      axios
        .post(
          'http://localhost:8000/api/v1/admin/backstage/admin-management/add-admin/',
          qs.stringify({
            phone_number: this.admin.phone_number,
            password: this.admin.password
          })
        )
        .then(response => {
          let _this = this
          this.wrong_count_down = 0
          this.success_count_down = 0
          if (response.data.new_admin_id) {
            _this.error_message = '添加成功'
            this.success_count_down = 3
            setTimeout(function () {
              _this.$router.push({ name: 'AdminManagement' })
            }, 3000)
          }
        })
        .catch(error => {
          let _this = this
          _this.wrong_count_down = 0
          _this.success_count_down = 0
          _this.error_message = error.response.data.message
          _this.wrong_count_down = 5
        })
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  text-align: left;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  padding-left: 15px;
  margin: 25px 0;
  color: #204269;
  text-align: left;
}

.form-group {
  padding-left: 15px;
  margin-top: 25px;
}

#save-btn {
  color: white;
}

.btn {
  margin-top: 40px;
  margin-right: 3px;
  margin-left: 15px;
  color: white;
  text-align: right;
  background-color: #449c44;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #4db14d;
}
</style>
