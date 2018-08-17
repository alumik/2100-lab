<template>
  <div class="html">
    <AdminNavbar id="navbar"/>
    <div id="body">
      <Menu/>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>订单列表</h1>
        <div class="table-div">
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
              <tr align="center">
                <td class="small-td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="small-td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="small-td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="small-td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td/>
                <td class="big-td">
                  <div>
                    <select
                      v-model="state"
                      class="selectpicker">
                      <option value="whole">全部</option>
                      <option value="finished">已完成</option>
                      <option value="refunded">已退款</option>
                    </select>
                  </div>
                </td>
                <td/>
              </tr>
              <tr
                v-for="order in orders"
                :key="order.id">
                <td>{{ order.order_code }}</td>
                <td>{{ order.course_code }}</td>
                <td>{{ order.course_name }}</td>
                <td>{{ order.user }}</td>
                <td>{{ order.charge }}</td>
                <td> {{ order.state }} </td>
                <td>
                  <button
                    type="button"
                    class="btn"
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
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
import Menu from '../components/menu'
export default {
  name: 'OrderManagement',
  components: { Menu, AdminNavbar, BreadCrumb, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '订单管理',
        active: true
      }],
      titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '用户名' },
        { label: '金额' },
        { label: '状态' },
        { label: '操作' }
      ],
      orders: [
        { order_code: '1001',
          course_code: 'SOFT1',
          course_name: '计算机',
          user: '小红',
          charge: '100.00',
          state: '已完成' },
        { order_code: '1002',
          course_code: 'ENGLISH2',
          course_name: '口语',
          user: '小明',
          charge: '120.00',
          state: '已退款' }
      ],
      rows: 2,
      state: null
    }
  },
  methods: {
    to_detail: function () {
      this.$router.push({ path: '/admin/order/detail' })
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 1300px;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  table {
    font-size: 1.2em;
    border: 1px solid #d3d9df;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1300px;
    height: calc(100% - 70px);
  }

  #management {
    flex-basis: 100%;
    padding: 0;
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

  select {
    width: 130px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }

  .html {
    height: 100%;
  }

  .table-div {
    padding-right: 15px;
    padding-left: 15px;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .small-td {
    width: 180px;
  }

  .big-td {
    width: 200px;
  }
</style>
