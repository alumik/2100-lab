<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>订单列表</h1>
      <div class="table-div">
        <Alert
          :count_down="wrong_count_down"
          :instruction="wrong"
          variant="danger"
          @decrease="wrong_count_down-1"
          @zero="wrong_count_down=0"/>
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
            <tr align="center">
              <td class="lg-td">
                <div class="input-group-sm">
                  <input
                    v-model="order_code"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div class="input-group-sm">
                  <input
                    v-model="course_code"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div class="input-group-sm">
                  <input
                    v-model="course_name"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div class="input-group-sm">
                  <input
                    v-model="user"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="s-td"/>
              <td class="s-td">
                <div>
                  <select
                    v-model="state"
                    class="selectpicker"
                    @change="search">
                    <option value="whole">全部</option>
                    <option value="finished">已完成</option>
                    <option value="refunded">已退款</option>
                  </select>
                </div>
              </td>
              <td class="s-td"/>
            </tr>
            <tr
              v-for="order in orders"
              :key="order.id">
              <td>{{ order.order_no }}</td>
              <td>{{ order.course_codename }}</td>
              <td>{{ order.course_title }}</td>
              <td>{{ order.customer_username }}</td>
              <td>{{ order.money }}</td>
              <td> {{ get_state(order.is_refunded) }} </td>
              <td>
                <button
                  type="button"
                  class="btn"
                  @click="to_detail(order.order_id + '')">
                  详情
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <Pagination
        :rows="rows"
        :perpage="per_page"
        @change="change_page"/>
    </div>
  </Basic>
</template>

<script>
import Pagination from '../../components/pagination'
import Basic from '../basic/basic'
import axios from 'axios'
import Alert from '../../components/alert'
export default {
  name: 'OrderManagement',
  components: { Alert, Basic, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '订单管理',
        active: true
      }],
      titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '用户名' },
        { label: '金额' },
        { label: '状态' },
        { label: '操作' }
      ],
      orders: [],
      rows: 0,
      order_code: '',
      course_code: '',
      course_name: '',
      user: '',
      state: '',
      page_jump: false,
      page: 1,
      per_page: 2,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  created () {
    const that = this
    axios.get('http://localhost:8000/api/v1/customers/backstage/order-management/get-order-list/',
      { params: {
        page_limit: that.per_page,
        page: that.page
      }})
      .then(function (response) {
        that.orders = response.data.content
        that.rows = response.data.count
      })
      .catch(function (error) {
        that.wrong = '加载订单失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    get_state: function (val) {
      if (val) {
        return '已退款'
      } else {
        return '已完成'
      }
    },
    search: function () {
      const that = this
      let state
      if (that.state === 'whole' || that.state === '') {
        state = '0'
      } else if (that.state === 'finished') {
        state = '1'
      } else {
        state = '2'
      }
      axios.get('http://localhost:8000/api/v1/customers/backstage/order-management/get-order-list/',
        {params: {
          order_no: that.order_code,
          course_codename: that.course_code,
          course_title: that.course_name,
          customer_username: that.user,
          is_refunded: state,
          page_limit: that.per_page,
          page: that.page
        }})
        .then(function (response) {
          that.orders = response.data.content
          that.rows = response.data.count
        })
        .catch(function (error) {
          that.wrong = '查询订单失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'OrderDetail', query: { order_id: val } })
    },
    change_page: function (page) {
      this.page = page
      this.search()
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

  td {
    vertical-align: middle;
  }

  table {
    font-size: 1.2em;
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

  select {
    width: 130px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }

  .table-div {
    padding-right: 15px;
    padding-left: 15px;
    overflow-x: scroll;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .s-td {
    width: 100px;
  }

  .md-td {
    width: 180px;
  }

  .lg-td {
    width: 420px;
  }
</style>
