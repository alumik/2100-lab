<template>
  <div class="father">
    <label class="head-text">新增管理员</label>
    <form class="write">
      <div>
        <label class="short-text">管理员手机号</label>
        <input
          class="input"
          type="text">
      </div>
      <div>
        <label class="short-text">管理员密码</label>
        <input
          class="input"
          type="text">
      </div>
      <div>
        <label>再次输入密码</label>
        <input
          class="input"
          type="text">
      </div>
      <button
        type="button"
        class="btn btn-primary btn-sm"
      >保存</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AddAdmin'
}
</script>

<style scoped>
  .father {
    min-width: 800px;
  }

  .head-text {
    margin-bottom: 4%;
    margin-left: -750px;
  }

  .short-text {
    padding-right: 17px;
  }

  .input {
    margin-left: 100px;
  }

  .write {
    margin-left: -400px;
  }

  .btn {
    margin-top: 2%;
    margin-left: -380px;
  }
</style>
