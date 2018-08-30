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
  /**
   * @returns {
   * {
   * items: *[], 路由管理
   * admin: { 管理员信息保存集合
   * phone_number: null, 手机号不能为空
   * password: null, 密码不能为空
   * password_again: null 第二次输入密码不能为空且必须与第一次输入密码相同
   * },
   * wrong_count_down: number, 失败倒计时秒数
   * success_count_down: number, 成功倒计时秒数
   * error_message: string 信息报错提示信息
   * }
   * }
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
  /**
   * 记录使用的所有函数方法
   * check_format
   * send_message
   * init_error_message
   **/
  methods: {
    /**
     * 函数用于输入检验数据格式：
     * 手机号不可为空
     * 密码不可为空
     * 再次输入密码不可为空且必须与第一次输入密码相同
     *
     * 格式检验通过之后调用发送函数
     */
    check_format: function () {
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
    /**
     *函数用于向后端发送一个请求
     * 请求内容为用户输入的手机号和密码
     * 捕获回应后会显示添加成功信息，之后重定向
     * 捕获错误后会发出错误提示
     */
    send_message: function () {
      axios
        .post(
          'http://localhost/api/v1/admin/backstage/admin-management/add-admin/',
          qs.stringify({
            phone_number: this.admin.phone_number,
            password: this.admin.password
          })
        )
        .then(response => {
          let _this = this
          _this.wrong_count_down = 0
          _this.success_count_down = 0
          _this.error_message = '添加成功'
          _this.success_count_down = 3
          _this.$router.push({ name: 'AdminManagement' })
        })
        .catch(error => {
          let _this = this
          _this.wrong_count_down = 0
          _this.success_count_down = 0
          _this.error_message = this.init_error_message(error.response.data.message)
          _this.wrong_count_down = 5
        })
    },
    /**
     *信息转换函数 将错误信息转换为中文
     * @param message 后端发来的错误信息
     * @returns {string} 转换为的中文
     */
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        case 'Not a valid phone number.':
          return '无效的手机号'
        case 'Invalid password.':
          return '无效的密码'
        case 'Admin is already registered.':
          return '该用户已被注册'
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
  padding-left: 15px;
  margin-top: 25px;
  margin-bottom: 60px;
  color: #204269;
  text-align: left;
}

label {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
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
  background-color: #4db14d;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #449c44;
}
</style>
