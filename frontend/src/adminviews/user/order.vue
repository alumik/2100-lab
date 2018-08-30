<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>相关订单</h1>
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
  name: 'Order',
  components: { Alert, Basic, Pagination },
  data () {
    return {
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
          href: '/admin/user/detail?user_id=' + this.$route.query.user_id
        },
        {
          text: '相关订单',
          active: true
        }
      ],
      titles: [
        { label: '订单编号' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '金额' },
        { label: '状态' }
      ],
      orders: [],
      rows: 0,
      page: 1,
      per_page: 15,
      wrong_count_down: 0,
      dismiss_second: 5,
      wrong: '',
      num_pages: 0
    }
  },
  /**
   * 该函数初始化用户相关订单页面，
   * 向后端通过get方法发送当前页面用户ID，当前页数以及单页最大数据量的数据，
   * 获得后端发送的订单数据、数据总条数及总页数，
   * 捕捉错误并进行相应提示。
   */
  created () {
    const that = this
    axios
      .get(
        'http://localhost/api/v1/customers/backstage/customer-management/get-customer-order-list/',
        {
          params: {
            customer_id: that.$route.query.user_id,
            page: that.page,
            page_limit: that.per_page
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
        if (error.response.data.message === 'Object not found.') {
          that.wrong = '该用户不存在，无法查找订单信息！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.wrong = '获取此用户的订单信息失败！' + error
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数接收Boolean类型的参数，
     * 返回表示订单是否退款的字符串。
     * @param val
     * @returns {string}
     */
    compute_state: function (val) {
      if (val) {
        return '已退款'
      } else {
        return '未退款'
      }
    },
    /**
     * 该函数实现页面的跳转，
     * 接收表示跳转后页数的参数，
     * 更改当前页数，进行查询操作刷新页面数据。
     * @param page
     */
    change_page: function (page) {
      this.page = page
      const that = this
      axios
        .get(
          'http://localhost/api/v1/customers/backstage/customer-management/get-customer-order-list/',
          {
            params: {
              customer_id: that.$route.query.user_id,
              page: that.page,
              page_limit: that.per_page
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
          if (error.response.data.message === 'Object not found.') {
            that.wrong = '该用户不存在，无法查找订单信息！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.wrong = '获取此用户的订单信息失败！'
            that.wrong_count_down = that.dismiss_second
          }
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

h1,
h6 {
  color: #23527c;
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

.table thead tr {
  font-weight: bold;
  color: #999;
}

.s-td {
  width: 100px;
}

.md-td {
  width: 150px;
}

.lg-td {
  width: 350px;
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
