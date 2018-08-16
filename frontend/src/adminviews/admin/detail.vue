<template>
  <div>
    <div>
      <AdminNavbar
        style="min-width: 500px;"/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="myrow" >
          <h2 class="sentence">管理员详情</h2>
          <div class="button_group">
            <button
              type="button"
              class="row btn btn-sm"
              @click="jump(1)"
            >分配权限</button>
            <button
              type="button"
              class="row btn btn-sm"
              @click="jump(2)"
            >修改密码</button>
            <button
              type="button"
              class="row btn btn-sm"
              @click="jump(3)"
            >删除管理员</button>
          </div>
        </div>
        <div class="table_div">
          <table
            class="table table-striped table-hover"
            width="100%">
            <tbody>
              <tr>
                <td class="head-td">
                  管理员ID
                </td>
                <td class="content-td">
                  {{ admin.ID }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  管理员手机号
                </td>
                <td class="content-td">
                  {{ admin.name }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  添加时间
                </td>
                <td class="content-td">
                  {{ admin.create_time }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  修改时间
                </td>
                <td class="content-td">
                  {{ admin.change_time }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  权限
                </td>
                <td class="content-td">
                  {{ admin.authority }}
                </td>
              </tr>
            </tbody>
          </table>
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
  name: 'AdminDetail',
  components: {BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      admin: {
        'ID': '000001',
        'name': 'DINGQUAN',
        'create_time': '2018-08-13',
        'change_time': '2018-08-13',
        'authority': 'askcnkj'
      },
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '管理员详情',
        active: true
      }]
    }
  },
  methods: {
    jump: function (id) {
      switch (id) {
        case 1:
          this.$router.push({name: 'DistributeAuthority'})
          break
        case 2:
          this.$router.push({name: 'ChangeCode'})
          break
      }
    }
  }
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    padding: 0;
  }

  .sentence {
    margin-left: 25px;
  }

  .myrow {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 60px;
    margin-bottom: 100px;
  }

  .head-td {
    width: 35%;
  }

  .content-td {
    width: 65%;
  }

  .button_group {
    display: flex;
  }

  .btn {
    margin-right: 25px;
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

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }
</style>
