<template>
  <div>
    <h2>新增管理员</h2>
    <form
      method="post">
      <div class="form-group">
        <label
          class="form-check-label"
          for="telephone">管理员手机号</label>
        <input
          id="telephone"
          v-model="admin.telephone"
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
        type="submit"
        class="btn btn-sm"
      >保存</button>
    </form>
  </div>

</template>

<script>
export default {
  name: 'AddAdminBasic',
  data: function () {
    return {
      admin: {
        telephone: null,
        password: null,
        password_again: null
      },
      error_messages: []
    }
  }
}
</script>

<style scoped>
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
