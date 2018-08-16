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
        <div class="title">
          <h1>用户详情</h1>
          <div class="buttons">
            <button
              v-b-modal.authenticate
              type="button"
              class="btn btn-lg"
              style="margin-right: 10px;">
              认证用户
            </button>
            <b-modal
              id="authenticate"
              ref="modal"
              title="认证理由"
              centered
              ok-title="确认"
              cancel-title="关闭">
              <p id="authenticate_confirm">您确定要认证此用户吗？</p>
            </b-modal>
            <button
              v-if="is_banned"
              type="button"
              class="btn btn-lg"
              style="margin-right: 10px;"
              @click="change_banned">
              取消禁言
            </button>
            <button
              v-b-modal.ban
              v-else
              type="button"
              class="btn btn-lg"
              style="margin-right: 10px;">
              禁言用户
            </button>
            <b-modal
              id="ban"
              ref="modal"
              title="确认禁言"
              centered
              ok-title="确定"
              cancel-title="取消"
              @ok="change_banned">
              <p id="ban_confirm">您确定要禁言此用户吗？</p>
            </b-modal>
            <button
              v-b-modal.delete
              type="button"
              class="btn btn-lg"
              style="margin-right: 10px;">
              删除用户
            </button>
            <b-modal
              id="delete"
              ref="modal"
              title="确认删除"
              centered
              ok-title="确定"
              cancel-title="取消">
              <p id="delete_confirm">您确定要删除此用户吗？</p>
            </b-modal>
          </div>
        </div>
        <div class="table_div">
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
            style="margin-right: 10px;"
            @click="to_order">
            查看更多
          </button>
        </div>
        <div class="table_div">
          <table
            id="order_table"
            class="table table-striped table">
            <thead>
              <tr style="background-color: #6c757d; color: white; font-weight: bold;">
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
              style="margin-right: 10px;"
              @click="to_course">
              查看更多
            </button>
          </div>
        </div>
        <div class="table_div">
          <table
            id="study_table"
            class="table table-striped">
            <thead>
              <tr style="background-color: #6c757d; color: white; font-weight: bold;">
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
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'UserDetail',
  components: {BreadCrumb, AdminNavbar, Menu},
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
        href: '/admin'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: '用户详情',
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
      is_banned: true
    }
  },
  methods: {
    change_banned () {
      this.is_banned = !this.is_banned
    },
    to_course () {
      this.$router.push('/admin/user/detail/course')
    },
    to_order () {
      this.$router.push('/admin/user/detail/order')
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
    justify-content: flex-end;
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

  img {
    width: 40px;
  }

  #delete_confirm,
  #ban_confirm,
  #authenticate_confirm {
    text-align: left;
  }

  #order_table,
  #study_table {
    border: 1px solid #d3d9df;
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

  .title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
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
