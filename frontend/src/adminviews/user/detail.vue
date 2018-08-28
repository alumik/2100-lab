<template>
  <Basic :items="items">
    <div class="body">
      <div class="title">
        <h1>用户详情</h1>
        <div class="buttons">
          <a
            v-if="is_vip"
            id="authenticated-button"
            class="btn"
            @click="authenticate_user">
            <simple-line-icons
              icon="action-undo"
              color="black"
              class="icon"
              size="small"/>
            取消认证
          </a>
          <a
            v-b-modal.authenticate
            v-else
            id="authenticate-button"
            class="btn">
            <simple-line-icons
              icon="user-following"
              color="white"
              class="icon"
              size="small"/>
            认证用户
          </a>
          <a
            v-if="is_banned"
            id="banned-button"
            class="btn"
            @click="ban_user">
            <simple-line-icons
              icon="action-undo"
              color="black"
              class="icon"
              size="small"/>
            取消禁言
          </a>
          <a
            v-b-modal.ban
            v-else
            id="ban-button"
            class="btn">
            <simple-line-icons
              icon="action-undo"
              color="white"
              class="icon"
              size="small"/>
            禁言用户
          </a>
          <a
            v-if="is_deleted"
            id="deleted-button"
            class="btn">
            <simple-line-icons
              icon="trash"
              color="black"
              class="icon"
              size="small"/>
            已删除
          </a>
          <a
            v-b-modal.delete
            v-else
            id="delete-button"
            class="btn">
            <simple-line-icons
              icon="trash"
              color="white"
              class="icon"
              size="small"/>
            删除用户
          </a>
        </div>
      </div>
      <ConfirmModal
        id="authenticate"
        title="确认认证"
        text="您确定要认证此用户吗？"
        @click="authenticate_user"/>
      <ConfirmModal
        id="delete"
        title="确认删除"
        text="您确定要删除此用户吗？"
        @click="delete_user"/>
      <ConfirmModal
        id="ban"
        title="确认禁言"
        text="您确定要禁言此用户吗？"
        @click="ban_user"/>
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
        <table
          id="detail-table"
          class="table">
          <tbody class="w-100">
            <tr class="row mx-0">
              <td class="col-3">头像</td>
              <td class="col-9">
                <img :src="avatar">
              </td>
            </tr>
            <tr
              v-for="n in titles.length"
              :key="n"
              class="row mx-0">
              <td class="col-3">{{ titles[n-1] }}</td>
              <td class="col-9">{{ user[n-1] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="title">
        <h2>相关订单</h2>
        <a
          id="order"
          class="btn"
          @click="to_order">
          <simple-line-icons
            icon="bubble"
            color="#5b9bd1"
            class="icon"
            size="small"/>
          查看更多
        </a>
      </div>
      <div class="table-div">
        <table
          id="order-table"
          class="table table-striped">
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
          <a
            id="course"
            class="btn"
            @click="to_course">
            <simple-line-icons
              icon="bubble"
              color="#5b9bd1"
              class="icon"
              size="small"/>
            查看更多
          </a>
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
  components: { Alert, Basic, ConfirmModal, BreadCrumb, AdminNavbar, Menu },
  data () {
    return {
      titles: ['用户名', '手机号码', '奖励金', '注册时间', '修改时间'],
      user: new Array(5),
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '用户管理',
          href: '/admin/user'
        },
        {
          text: this.$route.query.user_id,
          active: true
        }
      ],
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
      is_deleted: false,
      avatar: ''
    }
  },
  created () {
    const that = this
    axios
      .get(
        'http://localhost/api/v1/customers/backstage/customer-management/get-customer-detail/',
        {
          params: {
            customer_id: that.$route.query.user_id
          }
        }
      )
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
          that.avatar = that.$store.state.address + response.data.customer_info.avatar
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
      this.$router.push({
        name: 'Course',
        query: { user_id: this.$route.query.user_id }
      })
    },
    to_order () {
      this.page_jump_order = true
      this.$router.push({
        name: 'Order',
        query: { user_id: this.$route.query.user_id }
      })
    },
    authenticate_user: function () {
      const that = this
      axios
        .post(
          'http://localhost/api/v1/customers/backstage/customer-management/toggle-vip/',
          qs.stringify({
            customer_id: that.$route.query.user_id
          })
        )
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
      axios
        .post(
          'http://localhost/api/v1/customers/backstage/customer-management/toggle-banned/',
          qs.stringify({
            customer_id: that.$route.query.user_id
          })
        )
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
      axios
        .post(
          'http://localhost/api/v1/customers/backstage/customer-management/delete-customer/',
          qs.stringify({
            customer_id: that.$route.query.user_id
          })
        )
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
.body {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  margin: 25px 0;
}

h1,
h2 {
  color: #204269;
  text-align: left;
}

.buttons {
  display: inline-block;
}

.btn {
  display: inline-block;
  margin-left: 3px;
  color: white;
  border: 1px solid #d3d9df;
}

.table-div {
  padding: 0 15px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

#detail-table {
  border-bottom: 1px solid #d3d9df;
}

td {
  font-size: 1rem;
  vertical-align: middle;
}

img {
  width: 40px;
}

.col-3 {
  font-weight: bold;
  color: #337ab7;
  background-color: #f3f4f6;
}

.col-9 {
  color: #748085;
}

thead tr {
  font-weight: bold;
  color: #999;
}

#authenticate-button {
  color: white;
  background-color: #f37b1d;
}

#authenticate-button:hover,
#authenticate-button:active {
  color: white;
  background-color: #e0690c;
}

#ban-button,
#delete-button {
  color: white;
  background-color: #dd514c;
}

#ban-button:hover,
#ban-button:active,
#delete-button:hover,
#delete-button:active {
  color: white;
  background-color: #ba2d28;
}

#course,
#order {
  margin-right: 2px;
  margin-left: 2px;
  color: #5b9bd1;
  border: 1px solid #d3d9df;
}

#course:hover,
#course:active,
#order:hover,
#order:active {
  background-color: rgba(91, 155, 209, 0.2);
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
