<!--suppress ALL -->
<template>
  <div style="min-width: 500px">
    <b-navbar
      style="margin-bottom: 0px"
      toggleable="md"
      type="dark"
      variant="primary"
      class="navbar"
      sticky="true">
      <b-navbar-toggle target="nav_collapse"/>

      <b-navbar-brand
        href="#"
        disabled>2100实验室
      </b-navbar-brand>

      <b-collapse
        id="nav_collapse"
        is-nav>
        <b-navbar-nav class="ml-auto">

          <b-nav-text>管理员一</b-nav-text>

          <b-nav-item
            href="#"
            right>
            注销
          </b-nav-item>
        </b-navbar-nav>

      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import AdminManagement from '../admin/management'
import AdminDetail from '../admin/detail'
import AddAdmin from '../admin/addadmin'
export default {
  name: 'AdminNavbar',
  data: function () {
    return {
      AdminPage: AdminManagement
    }
  },
  methods: {
    admin_manage () {
      this.AdminPage = AdminManagement
      console.log('sklncjk')
    },
    add_new_admin () {
      this.AdminPage = AddAdmin
    },
    detail_information () {
      this.AdminPage = AdminDetail
    }
  }
}
</script>

<style>
  .navbar {
    /*background-color: #4fc8ff !important;*/
    position: sticky!important;
  }
</style>
