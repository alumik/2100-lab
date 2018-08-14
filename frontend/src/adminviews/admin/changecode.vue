<template>
  <div class="father">
    <AdminNavbar/>
    <label class="head-text row col-lg-5">修改密码</label>
    <div class="row col-lg-5">
      <form
        role="form">
        <div class="form-group">
          <label
            for="new-code"
            class="short-text">新密码</label>
          <input
            id="new-code"
            class="form-control"
            type="password">
        </div>
        <div class="form-group">
          <label
            for="new-code-again">重新输入密码</label>
          <input
            id="new-code-again"
            class="form-control"
            type="password">
        </div>
        <button
          type="submit"
          class="btn btn-primary"
        >保存</button>
      </form>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
export default {
  name: 'ChangeCode',
  components: {AdminNavbar}
}
</script>

<style scoped>
  .father {
    min-width: 800px;
  }

  .head-text {
    margin-left: 15px;
    font-size: 40px;
  }

  .short-text {
    padding-right: 45px;
  }

  .btn {
    margin-left: -40px;
  }

  .form-control {
    margin-left: 120px;
  }
</style>
