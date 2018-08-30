<template>
  <Basic :items="items">
    <div class="my-content">
      <h1>修改密码</h1>
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
        <a
          id="save-btn"
          class="btn"
          @click="submit_message">
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
  name: 'ChangeCode',
  components: { Alert, Basic },
  /**
   * @returns {
   * {
   * items: *[], 路由信息
   * new_password: null, 新输入的密码，不能为空
   * new_password_again: null, 重复的新输入的密码，不能为空，且必须与第一次密码相同
   * wrong_count_down: number, 失败时倒计时秒数
   * success_count_down: number, 成功时倒计时秒数
   * error_message: string 错误信息提示
   * }}
   */
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
          text: this.$route.query.admin_id.toString(),
          href:
            '/admin/adminmanagement/detail?admin_id=' +
            this.$route.query.admin_id.toString()
        },
        {
          text: '修改密码',
          active: true
        }
      ],
      new_password: null,
      new_password_again: null,
      wrong_count_down: 0,
      success_count_down: 0,
      error_message: ''
    }
  },
  /**
   * submit_message 发送请求函数
   * router_push 路由转换函数
   * init_error_message 错误信息转换函数
   */
  methods: {
    /**
     * 发送请求函数
     * 用户输入的新密码不能为空
     * 用户重复输入密码不能为空，且必须与第一次输入密码一致
     * 否则提示五秒钟错误
     *
     * 发送请求，包括用户ID和新密码
     * 得到回应，提示之后成功信息，路由函数页面跳转
     * 得到错误，提示五秒，信息转换函数返回错误信息内容
     */
    submit_message: function () {
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
        axios
          .post(
            'http://localhost/api/v1/admin/backstage/admin-management/change-admin-password/',
            qs.stringify({
              admin_id: this.$route.query.admin_id,
              new_password: this.new_password
            })
          )
          .then(response => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = response.data.message
            this.error_message = '修改密码成功'
            this.success_count_down = 3
            this.router_push()
          })
          .catch(error => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = this.init_error_message(error.response.data.message)
            this.wrong_count_down = 5
          })
      }
    },
    router_push () {
      this.$router.push({
        name: 'AdminDetail',
        query: { admin_id: this.$route.query.admin_id }
      })
    },
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        default:
          return '数据库查询出错'
      }
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
  margin: 25px 15px;
  color: #204269;
  text-align: left;
}

label {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
}

.form-group {
  margin-top: 60px;
  margin-left: 15px;
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
  background-color: #4db14d;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #449c44;
}
</style>
