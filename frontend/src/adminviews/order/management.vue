<template>
  <div>
    <AdminNavbar/>
    <div id="body">
      <Menu/>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>订单列表</h1>
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
              <td style="width: 27vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 27vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 27vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 27vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td/>
              <td style="width: 30vh;">
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
              <td>{{ order.orderCode }}</td>
              <td>{{ order.courseCode }}</td>
              <td>{{ order.courseName }}</td>
              <td>{{ order.user }}</td>
              <td>{{ order.charge }}</td>
              <td> {{ order.state }} </td>
              <td>
                <button
                  type="button"
                  class="btn-primary">
                  详情
                </button>
              </td>
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
        { orderCode: '1001',
          courseCode: 'SOFT1',
          courseName: '计算机',
          user: '小红',
          charge: '100.00',
          state: '已完成' },
        { orderCode: '1002',
          courseCode: 'ENGLISH2',
          courseName: '口语',
          user: '小明',
          charge: '120.00',
          state: '已退款' }
      ],
      rows: 2,
      state: null
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 2vh;
    margin-top: 4vh;
    margin-bottom: 4vh;
    text-align: left;
  }

  table {
    min-width: 160vh;
    font-size: 1.2em;
  }

  #body {
    display: flex;
    justify-content: space-between;
  }

  #management {
    flex-basis: 90%;
  }

  button {
    border-radius: 10px;
    box-shadow: #adb5bd inset;
  }

  select {
    width: 20vh;
    height: 4vh;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 2.5vh;
  }
</style>
