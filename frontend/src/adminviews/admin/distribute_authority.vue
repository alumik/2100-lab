<template>
  <div>
    <div class="my-nav">
      <AdminNavbar/>
    </div>
    <div class="my-menu">
      <div>
        <Menu/>
      </div>
      <div
        class="father container-fluid my-row">
        <BreadCrumb :items="items"/>
        <h1 class="header">分配权限</h1>
        <div class="text-left">
          <h6>管理员账号：{{ admin.ID }}</h6>
        </div>
        <div
          class="text-left my-auth-group">
          <h6>权限组：</h6>
          <div class="button_group">
            <button
              type="button"
              class="btn">A</button>
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
        <div class="text-left">
          <h6>权限</h6>
          <form>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-a"
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
              class="btn">保存</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'DistributeAuthority',
  components: {BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      admin: {
        ID: 'DingQuan'
      },
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '管理员详情',
        href: '/admin/adminmanagement/detail'
      }, {
        text: '分配权限',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  .my-nav {
    min-width: 500px;
  }

  .my-menu {
    display: flex;
  }

  .father {
    min-width: 500px;
    padding: 0;
    text-align: left;
  }

  .my-row {
    display: block;
  }

  .header {
    margin-top: 60px;
    margin-left: 120px;
  }

  .my-auth-group {
    display: flex;
  }

  .text-left {
    margin-top: 40px;
    margin-left: 120px;
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