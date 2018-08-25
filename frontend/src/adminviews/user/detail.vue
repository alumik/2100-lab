<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <div class="title">
        <h1>用户详情</h1>
        <div class="buttons">
          <button
            v-b-modal.redo_authenticate
            v-if="is_vip"
            type="button"
            class="btn btn-lg"
            @click="authenticate_user">
            取消认证
          </button>
          <button
            v-b-modal.authenticate
            v-else
            type="button"
            class="btn btn-lg">
            认证用户
          </button>
          <ConfirmModal
            id="authenticate"
            title="确认认证"
            text="您确定要认证此用户吗？"
            @click="authenticate_user"/>
          <button
            v-if="is_banned"
            type="button"
            class="btn btn-lg"
            @click="ban_user">
            取消禁言
          </button>
          <button
            v-b-modal.ban
            v-else
            type="button"
            class="btn btn-lg">
            禁言用户
          </button>
          <ConfirmModal
            id="ban"
            title="确认禁言"
            text="您确定要禁言此用户吗？"
            @click="ban_user"/>
          <button
            v-if="is_deleted"
            type="button"
            class="btn btn-lg">
            已删除
          </button>
          <button
            v-b-modal.delete
            v-else
            type="button"
            class="btn btn-lg">
            删除用户
          </button>
          <ConfirmModal
            id="delete"
            title="确认删除"
            text="您确定要删除此用户吗？"
            @click="delete_user"/>
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
      <div class="table-div">
        <table class="table table-bordered">
          <tbody class="w-100">
            <tr class="row mx-0">
              <td class="col-2">头像</td>
              <td class="col-10">
                <img src="http://localhost:8000/media/default/customers/avatars/2100_lab.jpg">
              </td>
            </tr>
            <tr
              v-for="n in titles.length"
              :key="n"
              class="row mx-0">
              <td class="col-2">{{ titles[n-1] }}</td>
              <td class="col-10">{{ user[n-1] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="title">
        <h2>相关订单</h2>
        <button
          id="order"
          type="button"
          class="btn"
          @click="to_order">
          查看更多
        </button>
      </div>
      <div class="table-div">
        <table
          id="order-table"
          class="table table-striped table">
          <thead>
            <tr>
              <td
                v-for="order_title in order_titles"
                :key="order_title.id">
                {{ order_title.label }}
              </td>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in orders"
              :key="order.id">
              <td class="lg-td">{{ order.order_no }}</td>
              <td class="md-td">{{ order.course_codename }}</td>
              <td class="md-td">{{ order.course_title }}</td>
              <td class="s-td">{{ order.money }}</td>
              <td class="s-td">{{ compute_state(order.is_refunded) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="title">
        <h2>相关课程</h2>
        <div class="buttons">
          <button
            id="course"
            type="button"
            class="btn"
            @click="to_course">
            查看更多
          </button>
        </div>
      </div>
      <div class="table-div">
        <table
          id="study-table"
          class="table table-striped">
          <thead>
            <tr>
              <td
                v-for="course_title in course_titles"
                :key="course_title.id">
                {{ course_title.label }}
              </td>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="course_log in course_logs"
              :key="course_log.id">
              <td class="md-td">{{ course_log.course_codename }}</td>
              <td class="md-td">{{ course_log.course_title }}</td>
              <td class="s-td">{{ course_log.progress }}</td>
              <td class="md-td">{{ compute_date(course_log.latest_learn) }}</td>
              <td class="md-td">{{ compute_burnt(course_log.is_burnt) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Basic>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import ConfirmModal from '../components/ConfirmModal'
import Basic from '../basic/basic'
import Alert from '../../components/alert'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'UserDetail',
  components: {Alert, Basic, ConfirmModal, BreadCrumb, AdminNavbar, Menu},
  data () {
    return {
      titles: ['用户名', '手机号码', '奖励金', '注册时间', '修改时间'],
      user: new Array(5),
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: this.$route.query.user_id,
        active: true
      }],
      order_titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '金额' },
        { label: '状态' }
      ],
      orders: [],
      course_titles: [
        { label: '课程代码' },
        { label: '课程名' },
        { label: '学习进度' },
        { label: '最近学习时间' },
        { label: '是否焚毁' }
      ],
      course_logs: [],
      page_jump_course: false,
      page_jump_order: false,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      success_count_down: 0,
      success: '',
      is_banned: false,
      is_vip: false,
      is_deleted: false
    }
  },
  created () {
    const that = this
    axios.get('http://localhost:8000/api/v1/customers/backstage/customer-management/get-customer-detail/',
      {params: {
        customer_id: that.$route.query.user_id
      }})
      .then(function (response) {
        if (response.data.message === 'Object not found.') {
          that.wrong = '无法查找到此用户的详情信息！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.user = that.compute_user(response.data.customer_info)
          that.is_banned = response.data.customer_info.is_banned
          that.is_vip = response.data.customer_info.is_vip
          that.is_deleted = response.data.customer_info.is_deleted
          that.orders = response.data.recent_orders
          that.course_logs = response.data.recent_learning_logs
        }
      })
      .catch(function (error) {
        that.wrong = '获取用户详情失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    compute_user: function (val) {
      let temp = []
      temp[0] = val.username
      temp[1] = val.phone_number
      temp[2] = val.reward_coin
      temp[3] = val.date_joined.slice(0, 10)
      temp[4] = val.updated_at.slice(0, 10)
      return temp
    },
    compute_state: function (val) {
      if (val) {
        return '已退款'
      } else {
        return '未退款'
      }
    },
    compute_date: function (val) {
      return val.slice(0, 10)
    },
    compute_burnt: function (val) {
      if (val) {
        return '已焚毁'
      } else {
        return '未焚毁'
      }
    },
    to_course: function () {
      this.page_jump_course = true
      this.$router.push({ name: 'Course', query: { user_id: this.$route.query.user_id } })
    },
    to_order () {
      this.page_jump_order = true
      this.$router.push({ name: 'Order', query: { user_id: this.$route.query.user_id } })
    },
    authenticate_user: function () {
      const that = this
      axios.post('http://localhost:8000/api/v1/customers/backstage/customer-management/toggle-vip/',
        qs.stringify({
          customer_id: that.$route.query.user_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '无法更改此用户认证信息！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.is_vip = !that.is_vip
            if (that.is_vip) {
              that.success = '您已经成功认证此用户！'
            } else {
              that.success = '您已经成功取消此用户的认证！'
            }
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '认证失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    ban_user: function () {
      const that = this
      axios.post('http://localhost:8000/api/v1/customers/backstage/customer-management/toggle-banned/',
        qs.stringify({
          customer_id: that.$route.query.user_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '无法禁言此用户！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.is_banned = !that.is_banned
            if (that.is_banned) {
              that.success = '您已经成功禁言此用户！'
            } else {
              that.success = '您已经成功取消此用户的禁言！'
            }
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '操作失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    delete_user: function () {
      const that = this
      axios.post('http://localhost:8000/api/v1/customers/backstage/customer-management/delete-customer/',
        qs.stringify({
          customer_id: that.$route.query.user_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '无法删除此用户！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.success = '您已经成功删除此用户！'
            that.is_deleted = true
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '删除失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    }
  }
}
</script>

<style scoped>
  h1,
  h2 {
    padding-left: 20px;
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

  img {
    width: 40px;
  }

  #order-table,
  #study-table {
    border: 1px solid #d3d9df;
  }

  .btn {
    margin-right: 10px;
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

  .title {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
  }

  .table-div {
    padding-right: 15px;
    padding-left: 15px;
    overflow-x: scroll;
  }

  .col-2 {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .col-10 {
    background-color: rgba(0, 0, 0, 0.05);
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  td {
    vertical-align: middle;
  }

  .s-td {
    width: 150px;
  }

  .md-td {
    width: 250px;
  }

  .lg-td {
    width: 500px;
  }
</style>
