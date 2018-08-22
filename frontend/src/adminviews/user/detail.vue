<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <div class="title">
        <h1>用户详情</h1>
        <div class="buttons">
          <button
            v-if="is_vip"
            type="button"
            class="btn btn-lg">
            已认证
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
            class="btn btn-lg">
            取消禁言
          </button>
          <button
            v-b-modal.ban
            v-else
            type="button"
            class="btn btn-lg">
            禁言用户
          </button>
          <b-modal
            id="ban"
            ref="modal"
            title="确认禁言"
            centered
            ok-title="确定"
            cancel-title="取消"
            @ok="ban_user">
            <p id="ban-confirm">您确定要禁言此用户吗？</p>
          </b-modal>
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
                <img :src="user.img">
              </td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">用户名</td>
              <td class="col-10">{{ user.name }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">手机号码</td>
              <td class="col-10">{{ user.phone }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">奖励金</td>
              <td class="col-10">{{ user.balance }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">注册时间</td>
              <td class="col-10">{{ user.register_time }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">修改时间</td>
              <td class="col-10">{{ user.change_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="title">
        <h2>相关订单</h2>
        <button
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
              <td>{{ order.order_code }}</td>
              <td>{{ order.course_code }}</td>
              <td>{{ order.course_name }}</td>
              <td>{{ order.charge }}</td>
              <td>{{ order.state }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="title">
        <h2>相关课程</h2>
        <div class="buttons">
          <button
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
              <td>{{ course_log.course_code }}</td>
              <td>{{ course_log.course_name }}</td>
              <td>{{ course_log.progress }}</td>
              <td>{{ course_log.time }}</td>
              <td>{{ course_log.state }}</td>
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
      user: { img: require('../../assets/logo.png'),
        name: '小红',
        phone: '13102250001',
        balance: '15.00',
        register_time: '2018-01-01',
        change_time: '2018-08-01' },
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
      orders: [
        { order_code: '0001', course_code: 'SOFT1', course_name: '计算机', charge: '110.00', state: '已完成' },
        { order_code: '0010', course_code: 'ENGLISH2', course_name: '口语', charge: '120.00', state: '已退款' }
      ],
      course_titles: [
        { label: '课程代码' },
        { label: '课程名' },
        { label: '学习进度' },
        { label: '最近学习时间' },
        { label: '是否焚毁' }
      ],
      course_logs: [
        { course_code: 'SOFT1', course_name: '计算机', progress: '01:22', time: '2018-08-14', state: '已焚毁' },
        { course_code: 'ENGLISH3', course_name: '英语写作', progress: '15:00', time: '2018-05-14', state: '未焚毁' }
      ],
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
    axios.get('',
      {params: {
        customer_id: that.$route.query.user_id
      }})
      .then(function (response) {
        if (response.data.message === 'Object not found.') {
          that.wrong = '无法查找到此用户的详情信息！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.user = response.data
          that.is_banned = response.data.is_banned
        }
      })
      .catch(function (error) {
        that.wrong = '获取用户详情失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
    axios.get('',
      {params: {
        customer_id: that.$route.query.user_id
      }})
      .then(function (response) {
        if (response.data.message === 'Object not found.') {
          that.wrong = '无法查找到此用户的订单信息！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.orders = response.data
        }
      })
      .catch(function (error) {
        that.wrong = '获取此用户的订单信息失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
    axios.get('',
      {params: {
        customer_id: that.$route.query.user_id
      }})
      .then(function (response) {
        if (response.data.message === 'Object not found.') {
          that.wrong = '无法查找到此用户的学习记录！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.orders = response.data
        }
      })
      .catch(function (error) {
        that.wrong = '获取此用户的学习记录失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    change_banned: function () {
      this.is_banned = !this.is_banned
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
      axios.post('',
        qs.stringify({
          customer_id: that.$route.query.user_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '无法认证此用户！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.success = '您已经成功认证此用户！'
            that.is_vip = true
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
      axios.post('',
        qs.stringify({
          customer_id: that.$route.query.user_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '无法禁言此用户！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.success = '您已经成功禁言此用户！'
            that.is_banned = true
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '禁言失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    delete_user: function () {
      const that = this
      axios.post('',
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
  .my-basic {
    min-width: 1000px;
  }

  h1,
  h2 {
    padding-left: 20px;
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

  img {
    width: 40px;
  }

  #ban-confirm {
    text-align: left;
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
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
  }

  .table-div {
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

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }
</style>
