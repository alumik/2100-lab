<template>
  <div>
    <AdminNavbar/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="detail">
        <BreadCrumb :items="items"/>
        <h1>订单详情</h1>
        <div class="buttons">
          <button
            v-b-modal.refund
            type="button"
            class="btn-primary btn-lg">
            退款
          </button>
          <b-modal
            id="refund"
            ref="modal"
            title="确认退款"
            centered
            ok-title="确定"
            cancel-title="取消">
            <p id="refund_confirm">您确定要进行退款操作吗？</p>
          </b-modal>
        </div>
        <table class="table table-bordered table-hover">
          <tbody class="w-100">
            <tr class="row mx-0">
              <td class="col-2">订单编号</td>
              <td class="col-10">{{ order.orderCode }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">课程代码</td>
              <td class="col-10">{{ order.courseCode }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">课程名</td>
              <td class="col-10">{{ order.courseName }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">用户名</td>
              <td class="col-10">{{ order.user }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">成交时间</td>
              <td class="col-10">{{ order.deal }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">退款时间</td>
              <td class="col-10">{{ order.refund }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">金额</td>
              <td class="col-10">{{ order.charge }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">状态</td>
              <td class="col-10">{{ order.state }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumb from '../../components/breadCrumb'
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
export default {
  name: 'OrderDetail',
  components: {AdminNavbar, BreadCrumb, Menu},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '订单管理',
        href: '/admin/order'
      }, {
        text: '订单详情',
        active: true
      }],
      order: { orderCode: '1001',
        courseCode: 'SOFT1',
        courseName: '计算机',
        user: '小红',
        charge: '100.00',
        deal: '2018-01-01',
        refund: null,
        state: '已完成' }
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 15px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    padding-bottom: 15px;
    text-align: right;
  }

  #refund_confirm {
    text-align: left;
  }

  #body {
    display: flex;
    justify-content: space-between;
  }

  #detail {
    flex-basis: 100%;
    padding-right: 15px;
  }

  table {
    min-width: 800px;
    padding-right: 15px;
    margin-left: 15px;
    font-size: 1.5em;
    text-align: center;
  }
</style>
