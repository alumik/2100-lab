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
      <b-pagination
        :total-rows="rows"
        :per-page="per_page"
        v-model="page"
        align="center"
        size="md"
        @input="change_page"/>
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
      rows: 0,
      user_id: '',
      user_name: '',
      phone: '',
      type: '',
      state: '',
      page_jump: false,
      page: 1,
      per_page: 15,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      num_pages: 0
    }
  },
  created () {
    const that = this
    axios
      .get(
        'http://localhost:8000/api/v1/customers/backstage/customer-management/get-customer-list/',
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
        that.wrong = '加载用户失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    get_type: function (val) {
      if (val) {
        return '认证用户'
      } else {
        return '普通用户'
      }
    },
    get_state: function (val) {
      if (val) {
        return '已禁言'
      } else {
        return '未禁言'
      }
    },
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'UserDetail', query: { user_id: val } })
    },
    change_page: function (page) {
      this.search()
    },
    search: function () {
      const that = this
      let type
      if (that.type === 'whole' || that.type === '') {
        type = '0'
      } else if (that.type === 'normal') {
        type = '1'
      } else {
        type = '2'
      }
      let state
      if (that.state === 'whole' || that.state === '') {
        state = '0'
      } else if (that.state === 'not_banned') {
        state = '1'
      } else {
        state = '2'
      }
      axios
        .get(
          'http://localhost:8000/api/v1/customers/backstage/customer-management/get-customer-list/',
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
          that.wrong = '查询用户失败！' + error
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

td {
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
