<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <div class="title">
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
      </div>
      <DetailTable
        :titles="titles"
        :data="order"/>
    </div>
  </Basic>
</template>

<script>
import BreadCrumb from '../../components/breadCrumb'
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import ConfirmModal from '../components/ConfirmModal'
import Basic from '../basic/basic'
import DetailTable from '../components/detail_table'
export default {
  name: 'OrderDetail',
  components: {DetailTable, Basic, ConfirmModal, AdminNavbar, BreadCrumb, Menu},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '订单管理',
        href: '/admin/order'
      }, {
        text: this.$route.query.order_id,
        active: true
      }],
      order: [ '1001', 'SOFT1', '计算机', '小红', '2018-01-01', null, '100.00', '已完成' ],
      titles: [ '订单编号', '课程代码', '课程名', '用户名', '成交时间', '退款时间', '金额', '状态' ]
    }
  }
}
</script>

<style scoped>
  .my-basic {
    min-width: 1000px;
  }

  .title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
  }

  h1 {
    padding-left: 15px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    text-align: right;
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
</style>
