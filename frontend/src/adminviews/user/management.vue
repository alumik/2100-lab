<template>
  <div>
    <AdminNavbar/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>用户列表</h1>
        <table class="table table-striped">
          <thead>
            <tr>
              <td
                v-for="title in titles"
                :key="title.id">
                {{ title.label }}
              </td>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in users"
              :key="user.id">
              <td>{{ user.user_id }}</td>
              <td>{{ user.user_name }}</td>
              <td>{{ user.phone }}</td>
              <td>{{ user.state }}</td>
            </tr>
          </tbody>
        </table>
        <Pagination :rows="rows"/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'UserManagement',
  components: {BreadCrumb, Menu, AdminNavbar},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '用户管理',
        active: 'true'
      }],
      titles: [
        { label: '用户ID' },
        { label: '用户名' },
        { label: '手机号' },
        { label: '禁言状态' },
        { label: '操作' }
      ],
      users: [
        { user_id: '001', user_name: '小红', phone: '13102250001', state: '已禁言' },
        { user_id: '002', user_name: '小明', phone: '13102250002', state: '未禁言' }
      ],
      rows: 20
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  table {
    min-width: 1300px;
    font-size: 1.2em;
  }

  #body {
    display: flex;
    justify-content: space-between;
  }

  #management {
    flex-basis: 100%;
    padding: 0;
  }
</style>
