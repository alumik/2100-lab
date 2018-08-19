<template>
  <div>
    <h2>修改密码</h2>
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
        class="btn btn-sm"
      >保存</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ChangeCodeBasic'
}
</script>

<style scoped>

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
