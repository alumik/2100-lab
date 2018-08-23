<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>修改密码</h2>
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
            for="newpassword">新密码</label>
          <input
            id="newpassword"
            v-model="new_password"
            class="input form-control col-lg-3"
            type="password">
        </div>
        <div class="form-group">
          <label
            class="form form-check-label"
            for="newpasswordagain">重新输入密码</label>
          <input
            id="newpasswordagain"
            v-model="new_password_again"
            class="form-control col-lg-3"
            type="password">
        </div>
        <button
          class="btn btn-sm"
          @click="submitMessage"
        >保存</button>
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
  name: 'ChangeCode',
  components: {Alert, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: this.$route.query.admin_id.toString(),
        href: '/admin/adminmanagement/detail?admin_id=' + this.$route.query.admin_id.toString()
      }, {
        text: '修改密码',
        active: true
      }],
      new_password: null,
      new_password_again: null,
      wrong_count_down: 0,
      success_count_down: 0,
      error_message: ''
    }
  },
  methods: {
    submitMessage: function () {
      if (this.new_password === null) {
        this.error_message = '请输入新密码'
        this.wrong_count_down = 5
      } else if (this.new_password_again === null) {
        this.error_message = '请再次输入新密码'
        this.wrong_count_down = 5
      } else if (this.new_password !== this.new_password_again) {
        this.error_message = '两次输入密码不一致'
        this.wrong_count_down = 5
      } else {
        axios.post('http://localhost:8000/api/v1/admin/backstage/admin-management/change-admin-password/',
          qs.stringify({
            admin_id: this.$route.query.admin_id,
            new_password: this.new_password
          })).then(
          response => {
            this.error_message = response.data.message
            this.$router.push({name: 'AdminDetail', query: {'admin_id': this.admin_id}})
          }
        ).catch(
          error => {
            this.error_message = error.response.message
            this.wrong_count_down = 5
          }
        )
      }
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
    margin-top: 60px;
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
