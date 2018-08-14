<template>
  <div>
    <div>
      <AdminNavbar/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container">
        <h1 class="head-text">新增管理员</h1>
        <form>
          <div class="form-group">
            <label
              class="form-check-label"
              for="telephone">管理员手机号</label>
            <input
              id="telephone"
              class="input form-control col-lg-3"
              type="text">
          </div>
          <div class="form-group">
            <label
              class="form form-check-label"
              for="password">管理员密码</label>
            <input
              id="password"
              class="form-control col-lg-3"
              type="password">
          </div>
          <div class="form-group">
            <label
              class="form form-check-label"
              for="passwordagain">再次输入密码</label>
            <input
              id="passwordagain"
              class="form-control col-lg-3"
              type="password">
          </div>
          <button
            type="submit"
            class="btn btn-primary btn-sm"
          >保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
export default {
  name: 'AddAdmin',
  components: {Menu, AdminNavbar}
}
</script>

<style>
  .father {
    min-width: 500px;
    text-align: left;
  }

  .head-text {
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .form-group {
    margin-top: 25px;
  }

  .btn {
    margin-top: 25px;
  }
</style>
