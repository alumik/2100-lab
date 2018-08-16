<template>
  <div>
    <AdminNavbar
      style="min-width: 800px;"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>用户列表</h1>
        <div class="table_div">
          <table class="table table-striped">
            <thead>
              <tr style="background-color: #6c757d; color: white; font-weight: bold;">
                <td
                  v-for="title in titles"
                  :key="title.id">
                  {{ title.label }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr align="center">
                <td style="width: 140px;">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td style="width: 140px;">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td style="width: 160px;">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td style="width: 200px;">
                  <div>
                    <select
                      v-model="state"
                      class="selectpicker">
                      <option value="whole">全部</option>
                      <option value="reserved">未删除</option>
                      <option value="deleted">已删除</option>
                    </select>
                  </div>
                </td>
                <td style="width: 200px;"/>
              </tr>
              <tr
                v-for="user in users"
                :key="user.id">
                <td>{{ user.user_id }}</td>
                <td>{{ user.user_name }}</td>
                <td>{{ user.phone }}</td>
                <td>{{ user.state }}</td>
                <td>
                  <button
                    type="button"
                    class="btn-primary"
                    @click="to_detail">
                    详情
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <Pagination :rows="rows"/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
export default {
  name: 'UserManagement',
  components: {BreadCrumb, Menu, AdminNavbar, Pagination},
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
  },
  methods: {
    to_detail: function () {
      this.$router.push('/admin/user/detail')
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  table {
    font-size: 1.2em;
    text-align: center;
    border: 1px solid #d3d9df;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 800px;
  }

  #management {
    flex-basis: 100%;
    padding: 0;
  }

  button {
    background-color: #0056b3;
    border-color: #0062cc;
    border-radius: 10px;
    outline: none;
    box-shadow: #0062cc inset;
  }

  select {
    width: 160px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }
</style>
