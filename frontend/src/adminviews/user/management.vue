<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>用户列表</h1>
      <div class="table-div">
        <div class="alert-div">
          <b-alert
            :show="wrong_count_down"
            class="my-alert"
            variant="danger"
            dismissible
            @dismissed="wrong_count_down=0"
            @dismiss_count_down="count_down_changed(wrong_count_down)">
            {{ wrong }}
          </b-alert>
        </div>
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
              <td class="s-td">
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
              <td class="lg-td">
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
              <td class="lg-td">
                <div>
                  <select
                    v-model="state"
                    class="selectpicker"
                    @change="search">
                    <option value="whole">全部</option>
                    <option value="is_banned">已禁言</option>
                    <option value="not_banned">未禁言</option>
                  </select>
                </div>
              </td>
              <td id="operation-td"/>
            </tr>
            <tr
              v-for="user in users"
              :key="user.id">
              <td>{{ user.user_id }}</td>
              <td>{{ user.user_name }}</td>
              <td>{{ user.phone }}</td>
              <td>{{ user.type }}</td>
              <td>{{ user.state }}</td>
              <td>
                <button
                  type="button"
                  class="btn"
                  @click="to_detail(user.user_id)">
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

export default {
  name: 'UserManagement',
  components: { Basic, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '用户管理',
        active: 'true'
      }],
      titles: [
        { label: '用户ID' },
        { label: '用户名' },
        { label: '手机号' },
        { label: '用户类型' },
        { label: '禁言状态' },
        { label: '操作' }
      ],
      users: [
        { user_id: '001', user_name: '13102250001', phone: '13102250001', type: '普通用户', state: '已禁言' },
        { user_id: '002', user_name: '13102250002', phone: '13102250002', type: '认证用户', state: '未禁言' }
      ],
      // users: [],
      rows: 0,
      user_id: '',
      user_name: '',
      phone: '',
      type: '',
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
    axios.get('', { params: {
      page_limit: that.per_page,
      page: that.page
    }})
      .then(function (response) {
        that.users = response.data.content
        that.rows = response.data.count
      })
      .catch(function (error) {
        that.wrong = '加载用户失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'UserDetail', query: { user_id: val } })
    },
    change_page: function (page) {
      this.page = page
      this.search()
    },
    count_down_changed: function (val) {
      const that = this
      let t = setInterval(function () {
        val -= 1
        if (that.val === 0) {
          clearInterval(t)
        }
      }, 1000)
    },
    search: function () {
      const that = this
      let type
      if (that.state === 'whole' || that.state === '') {
        type = '0'
      } else if (that.state === 'normal') {
        type = '1'
      } else {
        type = '2'
      }
      let state
      if (that.state === 'whole' || that.state === '') {
        state = '0'
      } else if (that.state === 'is_banned') {
        state = '1'
      } else {
        state = '2'
      }
      axios.get('',
        {params: {
          userid: that.user_id,
          username: that.user,
          phone: that.phone,
          type: type,
          state: state
        }})
        .then(function (response) {
          that.users = response.data.content
          that.rows = response.data.count
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
  .my-basic {
    min-width: 800px;
  }

  h1 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table-div {
    padding-right: 15px;
    padding-left: 15px;
  }

  table {
    font-size: 1.2em;
    text-align: center;
    border: 1px solid #d3d9df;
  }

  td {
    vertical-align: middle;
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
    width: 160px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .s-td {
    width: 140px;
  }

  .md-td {
    width: 180px;
  }

  .lg-td {
    width: 200px;
  }

  .alert-div {
    padding-right: 350px;
    padding-left: 350px;
  }

  .my-alert {
    min-width: 400px;
    max-width: 1000px;
  }
</style>
