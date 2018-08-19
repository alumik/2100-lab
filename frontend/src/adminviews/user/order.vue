<template>
  <div>
    <AdminNavbar id="navbar"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="study">
        <BreadCrumb :items="items"/>
        <h1>相关订单</h1>
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
              <tr
                v-for="order in orders"
                :key="order.id">
                <td>{{ order.order_code }}</td>
                <td>{{ order.course_code }}</td>
                <td>{{ order.course_name }}</td>
                <td>{{ order.charge }}</td>
                <td>{{ order.state }}</td>
              </tr>
            </tbody>
          </table>
          <Pagination :rows="rows"/>
        </div>
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
  name: 'Order',
  components: {Menu, AdminNavbar, BreadCrumb, Pagination},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: this.$route.query.user_id,
        href: '/admin/user/detail'
      }, {
        text: '相关订单',
        active: true
      }],
      titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '金额' },
        { label: '状态' }
      ],
      orders: [
        { order_code: '0001', course_code: 'SOFT1', course_name: '计算机', charge: '110.00', state: '已完成' },
        { order_code: '0010', course_code: 'ENGLISH2', course_name: '口语', charge: '120.00', state: '已退款' },
        { order_code: '0020', course_code: 'PHYSICS5', course_name: '小孔成像', charge: '100.00', state: '已完成' }
      ],
      rows: 10
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 1000px;
  }

  h1 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1000px;
  }

  #study {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
    text-align: center;
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
</style>
