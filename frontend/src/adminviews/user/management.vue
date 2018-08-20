<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>用户列表</h1>
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
              <td id="id-td">
                <div class="input-group-sm">
                  <input
                    v-model="user_id"
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td id="name-td">
                <div class="input-group-sm">
                  <input
                    v-model="user_name"
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td id="phone-td">
                <div class="input-group-sm">
                  <input
                    v-model="phone"
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td id="type-td">
                <div>
                  <select
                    v-model="type"
                    class="selectpicker">
                    <option value="whole">全部</option>
                    <option value="normal">普通用户</option>
                    <option value="authenticated">认证用户</option>
                  </select>
                </div>
              </td>
              <td id="state-td">
                <div>
                  <select
                    v-model="state"
                    class="selectpicker">
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
      <Pagination :rows="rows"/>
    </div>
  </Basic>
</template>

<script>
import Pagination from '../../components/pagination'
import Basic from '../basic/basic'
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
        { user_id: '001', user_name: '小红', phone: '13102250001', type: '普通用户', state: '已禁言' },
        { user_id: '002', user_name: '小明', phone: '13102250002', type: '认证用户', state: '未禁言' }
      ],
      rows: 20,
      user_id: '',
      user_name: '',
      phone: '',
      type: '',
      state: '',
      page_jump: false
    }
  },
  methods: {
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'UserDetail', query: { user_id: val } })
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

  #id-td,
  #name-td {
    width: 140px;
  }

  #phone-td {
    width: 180px;
  }

  #type-td,
  #state-td,
  #operation-td {
    width: 200px;
  }
</style>
