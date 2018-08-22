<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>修改密码</h2>
      <form>
        <div class="form-group">
          <label
            class="form-check-label"
            for="newpassword">新密码</label>
          <input
            id="newpassword"
            v-model="new_password"
            class="input form-control col-lg-3"
            type="text">
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
          type="submit"
          class="btn btn-sm"
        >保存</button>
      </form>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
export default {
  name: 'ChangeCode',
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
        text: this.$route.query.admin_id.toString(),
        href: '/admin/adminmanagement/detail?admin_id=' + this.$route.query.admin_id.toString()
      }, {
        text: '修改密码',
        active: true
      }],
      new_password: null,
      new_password_again: null
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
