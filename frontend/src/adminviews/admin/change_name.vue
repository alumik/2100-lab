<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>修改管理员名</h2>
      <form>
        <div class="form-group">
          <label
            class="form-check-label"
            for="newname">原管理员名：{{ old_name }}</label>
        </div>
        <div class="form-group">
          <label
            class="form-check-label"
            for="newname">新管理员名</label>
          <input
            id="newname"
            v-model="new_name"
            class="input form-control col-lg-3"
            type="text">
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
  name: 'ChangeName',
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
        text: '修改管理员名',
        active: true
      }],
      new_name: null,
      old_name: null
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
