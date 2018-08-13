<!--suppress ALL -->
<template>
  <div>
    <b-navbar
      toggleable="md"
      type="dark"
      variant="info"
      class="navbar">
      <b-navbar-toggle target="nav_collapse"/>

      <b-navbar-brand
        href="#"
        disabled>2100实验室 管理后台
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
    <b-card no-body>
      <b-tabs
        pills
        card
        vertical>
        <b-tab
          title="课程管理"
          active>
          kasnkca
        </b-tab>
        <b-tab title="留言管理">
          Tab Contents 2
        </b-tab>
        <b-tab title="用户管理">
          Tab Contents 2
        </b-tab>
        <b-tab title="订单管理">
          Tab Contents 2
        </b-tab>
        <b-tab
          title="管理员管理"
          @click="admin_manage">
          <li
            :is="AdminPage"
            @add_new_admin="add_new_admin"
            @detail_information="detail_information"
          />
        </b-tab>
        <b-tab title="数据分析">
          Tab Contents 2
        </b-tab>
        <b-tab title="日志查询">
          Tab Contents 2
        </b-tab>
      </b-tabs>
    </b-card>
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
