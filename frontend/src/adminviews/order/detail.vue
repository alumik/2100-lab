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
            text="您确定要进行退款操作吗？"
            @click="refund"/>
        </div>
      </div>
      <b-alert
        :show="wrong_count_down"
        class="my-alert"
        variant="danger"
        dismissible
        @dismissed="wrong_count_down=0"
        @dismiss_count_down="count_down_changed(wrong_count_down)">
        {{ wrong }}
      </b-alert>
      <b-alert
        :show="success_count_down"
        class="my-alert"
        variant="success"
        dismissible
        @dismissed="success_count_down=0"
        @dismiss_count_down="count_down_changed(success_count_down)">
        {{ success }}
      </b-alert>
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
export default {
  name: 'OrderDetail',
  components: {DetailTable, Basic, ConfirmModal, AdminNavbar, BreadCrumb, Menu},
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
      // order: [ '1001', 'SOFT1', '计算机', '小红', '2018-01-01', null, '100.00', '已完成' ],
      order: [],
      titles: [ '订单编号', '课程代码', '课程名', '用户名', '成交时间', '退款时间', '金额', '状态' ],
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      success_count_down: 0,
      success: ''
    }
  },
  computed_order: function (val) {
    let temp = new Array(8)
    temp[0] = val.order_codename
    temp[1] = val.course_codename
    temp[2] = val.course_title
    temp[3] = val.username
    temp[4] = (val.created_at + '').slice(0, 10)
    if (val.deleted_at === null) {
      temp[6] = ''
    } else {
      temp[6] = (val.deleted_at + '').slice(0, 10)
    }
    temp[7] = val.spend
    if (val.is_refunded) {
      temp[8] = '已退款'
    } else {
      temp[8] = '已完成'
    }
  },
  created () {
    const that = this
    axios.get('',
      {params: {
        order_id: that.$route.query.order_id
      }})
      .then(function (response) {
        that.order = that.computed_order(response.data)
      })
      .catch(function (error) {
        that.wrong = '获取订单详情失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    refund: function () {
      const that = this
      axios.get('',
        {params: {
          order_id: that.$route.query.order_id
        }})
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            that.success = '您已经成功退款。'
            that.success_count_down = that.dismiss_second
          } else {
            that.wrong = '你所要退款的留言不存在，删除失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '退款失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
      this.search()
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

  .my-alert {
    padding-right: 15px;
    padding-left: 15px;
  }
</style>
