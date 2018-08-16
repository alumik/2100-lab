<template>
  <div>
    <AdminNavbar
      style="min-width: 1000px;"/>
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
            class="btn btn-lg">
            退款
          </button>
          <ConfirmModal
            id="refund"
            title="确认退款"
            text="您确定要进行退款操作吗？"/>
        </div>
        <div class="table_div">
          <table class="table table-bordered">
            <tbody class="w-100">
              <tr class="row mx-0">
                <td class="col-2">订单编号</td>
                <td class="col-10">{{ order.order_code }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">课程代码</td>
                <td class="col-10">{{ order.course_code }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">课程名</td>
                <td class="col-10">{{ order.course_name }}</td>
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
  </div>
</template>

<script>
import BreadCrumb from '../../components/breadCrumb'
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import ConfirmModal from '../components/ConfirmModal'
export default {
  name: 'OrderDetail',
  components: {ConfirmModal, AdminNavbar, BreadCrumb, Menu},
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
      order: { order_code: '1001',
        course_code: 'SOFT1',
        course_name: '计算机',
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
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    padding-right: 15px;
    padding-bottom: 15px;
    text-align: right;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1000px;
  }

  #detail {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
    text-align: center;
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

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  .col-2 {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .col-10 {
    background-color: rgba(0, 0, 0, 0.05);
  }
</style>
