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
  name: 'ChangeCode',
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
        text: '管理员详情',
        href: '/admin/adminmanagement/detail'
      }, {
        text: '修改密码',
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

  .head-text {
    margin-top: 60px;
    margin-bottom: 60px;
    margin-left: 25px;
  }

  .form-group {
    margin-top: 60px;
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
