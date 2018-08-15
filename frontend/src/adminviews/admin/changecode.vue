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
        <h1 class="head-text">修改密码</h1>
        <form>
          <div class="form-group">
            <label
              class="form-check-label"
              for="newpassword">新密码</label>
            <input
              id="newpassword"
              class="input form-control col-lg-3"
              type="text">
          </div>
          <div class="form-group">
            <label
              class="form form-check-label"
              for="newpasswordagain">重新输入密码</label>
            <input
              id="newpasswordagain"
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
  name: 'ChangeCode',
  components: {Menu, AdminNavbar}
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    text-align: left;
  }

  .head-text {
    margin-top: 60px;
    margin-bottom: 60px;
  }

  .form-group {
    margin-top: 60px;
  }

  .btn {
    margin-top: 25px;
  }
</style>
