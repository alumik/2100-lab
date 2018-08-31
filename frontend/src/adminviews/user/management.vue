<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>用户列表</h1>
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
              <td class="s-td">
                <div class="input-group-sm">
                  <input
                    v-model="user_id"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div class="input-group-sm">
                  <input
                    v-model="user_name"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div class="input-group-sm">
                  <input
                    v-model="phone"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="md-td">
                <div>
                  <select
                    v-model="type"
                    class="selectpicker"
                    @change="search">
                    <option value="whole">全部</option>
                    <option value="normal">普通用户</option>
                    <option value="authenticated">认证用户</option>
                  </select>
                </div>
              </td>
              <td class="md-td">
                <div>
                  <select
                    v-model="state"
                    class="selectpicker"
                    @change="search">
                    <option value="whole">全部</option>
                    <option value="not_banned">未禁言</option>
                    <option value="is_banned">已禁言</option>
                  </select>
                </div>
              </td>
              <td class="s-td"/>
            </tr>
            <tr
              v-for="user in users"
              :key="user.id">
              <td>{{ user.customer_id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.phone_number }}</td>
              <td>{{ get_type(user.is_vip) }}</td>
              <td>{{ get_state(user.is_banned) }}</td>
              <td>
                <a
                  id="detail-button"
                  class="btn"
                  @click="to_detail(user.customer_id + '')">
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
  name: 'UserManagement',
  components: { Alert, Basic, Pagination },
  /**
   * @returns {{
   * items: *[], 面包屑路由地址
   * titles: Array, 用户列表标题
   * users: Array, 用户列表数据
   * user_id: string，
   * user_name: string,
   * phone: string,
   * type: string,
   * state: string，
   * 用户列表查询条件数据
   * rows: number, 数据总条数
   * page: number, 当前页数
   * per_page: number, 单页数据条数
   * num_pages: number, 数据总页数
   * page_jump: boolean, 页面跳转标志
   * dismiss_second: number,
   * wrong_count_down: number,
   * wrong: string
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
          text: '用户管理',
          active: 'true'
        }
      ],
      titles: [
        { label: '用户ID' },
        { label: '用户名' },
        { label: '手机号' },
        { label: '用户类型' },
        { label: '禁言状态' },
        { label: '操作' }
      ],
      users: [],
      user_id: '',
      user_name: '',
      phone: '',
      type: '',
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
   * 该函数在初始化用户管理页面时被调用，
   * 通过get方法向后端发送单页最大数据量及当前页数的数据，
   * 并获得后端发送的用户数据，
   * 进行错误捕捉并进行相应提示。
   */
  created () {
    const that = this
    axios
      .get(
        'http://localhost/api/v1/customers/backstage/customer-management/get-customer-list/',
        {
          params: {
            page_limit: that.per_page,
            page: that.page
          }
        }
      )
      .then(function (response) {
        that.users = response.data.content
        that.rows = response.data.count
        if (response.data.num_pages === 0) {
          that.num_pages = 1
        } else {
          that.num_pages = response.data.num_pages
        }
      })
      .catch(function (error) {
        if (error) {
          that.wrong = '加载用户失败！'
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数接收Boolean类型的参数，
     * 返回表示是否被认证的字符串。
     * @param val
     * @returns {string}
     */
    get_type: function (val) {
      if (val) {
        return '认证用户'
      } else {
        return '普通用户'
      }
    },
    /**
     * 该函数接收Boolean类型的参数，
     * 返回表示是否被禁言的字符串。
     * @param val
     * @returns {string}
     */
    get_state: function (val) {
      if (val) {
        return '已禁言'
      } else {
        return '未禁言'
      }
    },
    /**
     * 该函数接收一个表示用户ID的参数，
     * 并跳转到相应用户ID的详情页面。
     * @param val
     */
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'UserDetail', query: { user_id: val } })
    },
    /**
     * 该函数接收一个表示页数的参数，
     * 更改当前页数，
     * 并进行查询操作刷新界面。
     * @param page
     */
    change_page: function (page) {
      this.page = page
      this.search()
    },
    /**
     * 该函数将表示用户类型的type变量的字符串转化为由相对应数字构成的字符串，
     * 返回转换后的字符串。
     * @returns {string}
     */
    get_type_data: function () {
      let type
      if (this.type === 'whole' || this.type === '') {
        type = '0'
      } else if (this.type === 'normal') {
        type = '1'
      } else {
        type = '2'
      }
      return type
    },
    /**
     * 该函数将表示禁言状态的state变量的字符串转化为由相对应数字构成的字符串，
     * 返回转换后的字符串。
     * @returns {string}
     */
    get_state_data: function () {
      let state
      if (this.state === 'whole' || this.state === '') {
        state = '0'
      } else if (this.state === 'not_banned') {
        state = '1'
      } else {
        state = '2'
      }
      return state
    },
    /**
     * 该函数通过get方法向后端发送表示用户ID、用户名、电话号码、是否为VIP、是否被禁言、单页最大数据量、当前页数的数据，
     * 并获得后端发送的用户数据、用户总数以及总页数的数据，
     * 并捕捉错误进行相应提示。
     */
    search: function () {
      const that = this
      let type = this.get_type_data()
      let state = this.get_state_data()
      axios
        .get(
          'http://localhost/api/v1/customers/backstage/customer-management/get-customer-list/',
          {
            params: {
              customer_id: that.user_id,
              username: that.user_name,
              phone_number: that.phone,
              is_vip: type,
              is_banned: state,
              page_limit: that.per_page,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.users = response.data.content
          that.rows = response.data.count
          if (response.data.num_pages === 0) {
            that.num_pages = 1
          } else {
            that.num_pages = response.data.num_pages
          }
        })
        .catch(function (error) {
          if (error) {
            that.wrong = '加载用户失败！'
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

thead tr {
  font-weight: bold;
  color: #999;
}

.s-td {
  width: 120px;
}

.md-td {
  width: 180px;
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
