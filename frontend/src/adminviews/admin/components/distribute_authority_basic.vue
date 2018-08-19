<template>
  <div>
    <div>
      <h2>分配权限</h2>
      <h4 class="my-text">管理员账号：{{ admin.ID }}</h4>
      <div
        class="my-auth-group">
        <h4 class="my-text">权限组：</h4>
        <div class="button_group my-text">
          <button
            type="button"
            class="btn"
            @click="chooseA">A</button>
          <button
            type="button"
            class="btn">B</button>
          <button
            type="button"
            class="btn">C</button>
          <button
            type="button"
            class="btn">D</button>
        </div>
      </div>
      <div>
        <h4 class="my-text">权限</h4>
        <form>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-a"
              ref="check_a"
              type="checkbox"
              class="custom-control-input form-control"
              name="a">
            <label
              class="custom-control-label form-check-label"
              for="check-a">a</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-b"
              type="checkbox"
              class="custom-control-input form-control"
              name="b">
            <label
              class="custom-control-label form-check-label"
              for="check-b">b</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-c"
              type="checkbox"
              class="custom-control-input form-control"
              name="c">
            <label
              class="custom-control-label form-check-label"
              for="check-c">c</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-d"
              type="checkbox"
              class="custom-control-input form-control"
              name="d">
            <label
              class="custom-control-label form-check-label"
              for="check-d">d</label>
          </div>
          <br>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-e"
              type="checkbox"
              class="custom-control-input form-control"
              name="e">
            <label
              class="custom-control-label form-check-label"
              for="check-e">e</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-f"
              type="checkbox"
              class="custom-control-input form-control"
              name="f">
            <label
              class="custom-control-label form-check-label"
              for="check-f">f</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-g"
              type="checkbox"
              class="custom-control-input form-control"
              name="g">
            <label
              class="custom-control-label form-check-label"
              for="check-g">g</label>
          </div>
          <div class="custom-control custom-checkbox custom-control-inline form-group">
            <input
              id="check-h"
              type="checkbox"
              class="custom-control-input form-control"
              name="h">
            <label
              class="custom-control-label form-check-label"
              for="check-h">h</label>
          </div>
          <br>
          <button
            type="submit"
            class="btn my-text">保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DistributeAuthorityBasic',
  data: function () {
    return {
      admin: {
        ID: 'DingQuan'
      },
      auth_text: []
    }
  },
  methods: {
    chooseA: function () {
      this.$refs.check_a.setAttribute('checked', true)
      this.auth_text.push('a')
    }
  }
}
</script>

<style scoped>
  .my-auth-group {
    display: flex;
  }

  .my-text {
    margin-top: 60px;
  }

  .btn {
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
