<template>
  <div>
    <div class="my-nav">
      <AdminNavbar/>
    </div>
    <div class="my-menu">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <h2 class="head-text">新增管理员</h2>
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
            class="btn btn-sm"
          >保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'AddAdmin',
  components: {BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '新增管理员',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    padding: 0;
    text-align: left;
  }

  .my-menu {
    display: flex;
  }

  .my-nav {
    min-width: 500px;
  }

  .head-text {
    margin-top: 40px;
    margin-bottom: 40px;
    margin-left: 25px;
  }

  .form-group {
    margin-top: 25px;
    margin-left: 25px;
  }

  .btn {
    margin-top: 25px;
    margin-left: 25px;
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
