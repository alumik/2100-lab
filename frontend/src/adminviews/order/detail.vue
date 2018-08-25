<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <div class="title">
        <h1>订单详情</h1>
        <div class="buttons">
          <button
            v-if="is_refunded"
            type="button"
            class="btn btn-lg">
            已退款
          </button>
          <button
            v-b-modal.refund
            v-else
            type="button"
            class="btn btn-lg">
            退款
          </button>
          <ConfirmModal
            id="refund"
            title="确认退款"
            text="您确定要进行退款操作吗？"
            @click="refund"/>
        </div>
      </div>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <Alert
        :count_down="success_count_down"
        :instruction="success"
        variant="success"
        @decrease="success_count_down-1"
        @zero="success_count_down=0"/>
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
import axios from 'axios'
import Alert from '../../components/alert'
import qs from 'qs'
export default {
  name: 'OrderDetail',
  components: {Alert, DetailTable, Basic, ConfirmModal, AdminNavbar, BreadCrumb, Menu},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '订单管理',
        href: '/admin/order'
      }, {
        text: this.$route.query.order_id,
        active: true
      }],
      order: [],
      titles: [ '订单编号', '课程代码', '课程名', '用户名', '成交时间', '退款时间', '金额', '状态' ],
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      success_count_down: 0,
      success: '',
      is_refunded: false
    }
  },
  created () {
    const that = this
    axios.get('http://localhost:8000/api/v1/customers/backstage/order-management/get-order-detail/',
      {params: {
        order_id: that.$route.query.order_id
      }})
      .then(function (response) {
        that.order = that.compute_order(response.data)
        that.is_refunded = response.data.is_refunded
      })
      .catch(function (error) {
        that.wrong = '获取订单详情失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    refund: function () {
      const that = this
      axios.post('http://localhost:8000/api/v1/customers/backstage/order-management/order-refund/',
        qs.stringify({ order_id: that.$route.query.order_id }))
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.success = '您已经成功退款。'
            that.is_refunded = true
            that.success_count_down = that.dismiss_second
          } else {
            that.wrong = '你所要退款的订单不存在，退款失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '退款失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
      axios.get('http://localhost:8000/api/v1/customers/backstage/order-management/get-order-detail/',
        {params: {
          order_id: that.$route.query.order_id
        }})
        .then(function (response) {
          that.order = that.compute_order(response.data)
          that.is_refunded = response.data.is_refunded
        })
        .catch(function (error) {
          that.wrong = '获取订单详情失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    compute_order: function (val) {
      let temp = new Array(8)
      temp[0] = val.order_no
      temp[1] = val.course_codename
      temp[2] = val.course_title
      temp[3] = val.customer_username
      temp[4] = (val.created_at + '').slice(0, 10)
      if (val.refunded_at === null) {
        temp[5] = ''
      } else {
        temp[5] = (val.refunded_at + '').slice(0, 10)
      }
      temp[6] = val.money
      if (val.is_refunded) {
        temp[7] = '已退款'
      } else {
        temp[7] = '已完成'
      }
      return temp
    }
  }
}
</script>

<style scoped>
  .title {
    display: flex;
    flex-wrap: wrap;
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
    flex-wrap: wrap;
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
