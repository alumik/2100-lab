<template>
  <div class="div1">
    <AdminNavbar
      style="min-width: 500px;"/>
    <div
      class="div2"
      style="display: flex;">
      <Menu/>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="head-row">
          <h3 class="list">管理员列表</h3>
          <button
            type="button"
            class="head-btn btn btn-primary btn-sm"
            @click="jump(-1)"
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
                @click="jump(admin.id)"
              >详情</button>
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
import Pagination from '../../components/pagination'
export default {
  name: 'AdminManagement',
  components: {Pagination, BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      admins: [
        {'id': 0, 'ID': '000000', 'name': 'DingQuan'},
        {'id': 1, 'ID': '000001', 'name': 'DingQuan1'},
        {'id': 2, 'ID': '000002', 'name': 'DingQuan2'},
        {'id': 3, 'ID': '000000', 'name': 'DingQuan3'},
        {'id': 4, 'ID': '000001', 'name': 'DingQuan4'},
        {'id': 5, 'ID': '000002', 'name': 'DingQuan5'},
        {'id': 6, 'ID': '000000', 'name': 'DingQuan6'},
        {'id': 7, 'ID': '000001', 'name': 'DingQuan7'},
        {'id': 8, 'ID': '000002', 'name': 'DingQuan8'}
      ],
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        active: true
      }],
      rows: 20
    }
  },
  methods: {
    jump: function (id) {
      console.log(id)
      if (id === -1) {
        this.$router.push({name: 'AddAdmin'})
      } else {
        this.$router.push({name: 'AdminDetail'})
      }
    }
  }
}
</script>

<style>
  .father {
    min-width: 500px;
    padding: 0;
  }

  .head-row {
    display: flex;
    justify-content: space-evenly;
    margin-top: 50px;
  }

  .head-btn {
    margin-left: 50%;
  }

  .row {
    display: flex;
    flex: 0 1 auto;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 60px;
  }

  .inner-btn {
    margin-top: 2%;
    margin-left: 50%;
  }

  .table {
    margin-top: 1%;
  }

  .div1 {
    height: 100%;
  }

  .div2 {
    height: calc(100% - 70px);
  }
</style>
