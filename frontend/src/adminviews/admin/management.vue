<template>
  <div>
    <div>
      <AdminNavbar/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <div class="row">
          <h3 class="list">管理员列表</h3>
          <button
            type="button"
            class="row head-btn btn btn-primary btn-sm"
            @click="add_new_admin"
          >新增管理员</button>
        </div>
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">管理员ID</th>
              <th scope="col">管理员手机号</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control col-xs-2"
                    placeholder="">
              </div></td>
              <td>
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control col-xs-2"
                    placeholder="">
                </div>
              </td><td>
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control col-xs-2"
                    placeholder="">
              </div></td>
            </tr>
            <tr
              v-for="admin in admins"
              :key="admin.id">
              <td>{{ admin.ID }}</td>
              <td>{{ admin.name }}</td>
              <button
                type="button"
                class="row inner-btn btn-primary btn-sm"
                @click="detail_information"
              >详情</button>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
</div></template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
export default {
  name: 'AdminManagement',
  components: {Menu, AdminNavbar},
  data: function () {
    return {
      admins: [
        {'ID': '000000', 'name': 'DingQuan'},
        {'ID': '000001', 'name': 'DingQuan1'},
        {'ID': '000002', 'name': 'DingQuan2'},
        {'ID': '000000', 'name': 'DingQuan3'},
        {'ID': '000001', 'name': 'DingQuan4'},
        {'ID': '000002', 'name': 'DingQuan5'},
        {'ID': '000000', 'name': 'DingQuan6'},
        {'ID': '000001', 'name': 'DingQuan7'},
        {'ID': '000002', 'name': 'DingQuan8'}
      ]
    }
  },
  methods: {
    add_new_admin () {
      this.$emit('add_new_admin')
    },
    detail_information () {
      this.$emit('detail_information')
    }
  }
}
</script>

<style>
  .father {
    min-width: 500px;
    padding: 0;
    margin-top: 40px;
  }

  .row {
    display: flex;
    flex: 0 1 auto;
    flex-direction: row;
    justify-content: space-around;
  }

  .list {
    margin-left: -18%;
  }

  .head-btn {
    margin-right: -18%;
  }

  .inner-btn {
    margin-top: 2%;
    margin-left: 50%;
  }

  .table {
    margin-top: 1%;
  }
</style>
