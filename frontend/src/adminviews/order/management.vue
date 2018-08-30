<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>订单列表</h1>
        </div>
        <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      </div>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <div class="table-div">
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
              <td>{{ compute_username(order.customer_username) }}</td>
              <td>{{ order.money }}</td>
              <td> {{ get_state(order.is_refunded) }} </td>
              <td>
                <a
                  id="detail-button"
                  class="btn"
                  @click="to_detail(order.order_id + '')">
                  <simple-line-icons
                    icon="bubble"
                    color="#5b9bd1"
                    class="icon"
                    size="small"/>
                  详情
                </a>
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
  /**
   * @returns {{
   * items: *[], 面包屑路由地址
   * titles: Array, 订单列表标题
   * orders: Array, 订单列表数据
   * order_code: string，
   * course_code: string,
   * course_name: string,
   * user: string,
   * state: string，
   * 订单列表查询条件数据
   * rows: number, 数据总条数
   * page: number, 当前页数
   * per_page: number, 单页数据条数
   * num_pages: number, 数据总页数
   * page_jump: boolean, 页面跳转标志
   * dismiss_second: number,
   * wrong_count_down: number,
   * wrong: string,
   * Alert组件所需参数
   * }}
   */
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '订单管理',
          active: true
        }
      ],
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
      order_code: '',
      course_code: '',
      course_name: '',
      user: '',
      state: '',
      page_jump: false,
      rows: 0,
      page: 1,
      per_page: 15,
      num_pages: 0,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  /**
   * 该函数在初始化订单管理页面时调用，
   * 通过post方法向后端发送每页最大数据量和当前页数，
   * 并接收后端返回的订单、订单总数及页面总页数的信息，
   * 并捕捉错误信息进行提示
   */
  created () {
    const that = this
    axios
      .get(
        'http://localhost/api/v1/customers/backstage/order-management/get-order-list/',
        {
          params: {
            page_limit: that.per_page,
            page: that.page
          }
        }
      )
      .then(function (response) {
        that.orders = response.data.content
        that.rows = response.data.count
        if (response.data.num_pages === 0) {
          that.num_pages = 1
        } else {
          that.num_pages = response.data.num_pages
        }
      })
      .catch(function (error) {
        if (error) {
          that.wrong = '加载订单失败！'
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数接收一个表示用户名的字符串，
     * 根据用户是否被删除返回处理过后的字符串类型的用户名
     * @param name
     * @returns {*}
     */
    compute_username: function (name) {
      let index = name.search('_deleted_')
      if (index !== -1) {
        return name.slice(0, index) + '（已删除）'
      } else {
        return name
      }
    },
    /**
     * 该函数接收一个boolean类型的参数，
     * 返回一个表示订单是否被退款的字符串
     * @param deleted
     * @returns {*}
     */
    get_state: function (val) {
      if (val) {
        return '已退款'
      } else {
        return '已完成'
      }
    },
    /**
     * 该函数在翻页或者查询时调用，
     * 通过get方法向后端发送表示订单编号、课程代码、课程名、用户名、是否退款、单页最大数据量及当前页数的数据，
     * 获得后端返回的查询过后的订单信息及符合条件的订单总条数，
     * 并捕捉错误进行判断，返回相应的提示信息。
     */
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
      axios
        .get(
          'http://localhost/api/v1/customers/backstage/order-management/get-order-list/',
          {
            params: {
              order_no: that.order_code,
              course_codename: that.course_code,
              course_title: that.course_name,
              customer_username: that.user,
              is_refunded: state,
              page_limit: that.per_page,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.orders = response.data.content
          that.rows = response.data.count
          if (response.data.num_pages === 0) {
            that.num_pages = 1
          } else {
            that.num_pages = response.data.num_pages
          }
        })
        .catch(function (error) {
          if (error) {
            that.wrong = '加载订单失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
    },
    /**
     * 该函数接收一个表示留言ID的参数，并跳转到该详情页面。
     * @param val
     */
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'OrderDetail', query: { order_id: val } })
    },
    /**
     * 该函数接收一个表示页数的参数，
     * 更改页数并进行查询操作。
     * @param page
     */
    change_page: function (page) {
      this.page = page
      this.search()
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

h1,
h6 {
  color: #204269;
  text-align: left;
}

h6 {
  font-weight: bold;
}

.table-div {
  padding: 0 15px;
  margin-bottom: 25px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

.table td {
  font-size: 1rem;
  vertical-align: middle;
}

.btn {
  margin-right: 2px;
  margin-left: 2px;
  border: 1px solid #d3d9df;
}

#detail-button {
  margin-right: 2px;
  margin-left: 2px;
  color: #5b9bd1;
  border: 1px solid #d3d9df;
}

#detail-button:hover,
#detail-button:active {
  background-color: rgba(91, 155, 209, 0.2);
}

select {
  width: 130px;
  height: 30px;
  color: #2c3e50;
  border: 1px solid #ced4da;
  border-radius: 5px;
  outline: none;
}

option {
  font-size: 18px;
}

.table thead tr {
  font-weight: bold;
  color: #999;
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

.head-title {
  display: flex;
  margin: 25px 0;
}

.head-container {
  padding: 0 15px;
  margin-bottom: 15px;
  text-align: left;
}
</style>
