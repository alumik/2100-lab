<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>管理员列表</h2>
      <Alert
        :count_down="wrong_count_down"
        :instruction="error_message"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <Alert
        :count_down="success_count_down"
        :instruction="error_message"
        variant="success"
        @decrease="success_count_down-1"
        @zero="success_count_down=0"/>
      <button
        id="head-btn"
        type="button"
        class="btn btn-sm"
        @click="jump(-1)"
      >新增管理员</button>
      <div class="table-div">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">管理员名称</th>
              <th scope="col">管理员手机号</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="input-group">
                  <input
                    v-model="username"
                    type="text"
                    class="form-control col-xs-2"
                    placeholder=""
                    @keyup.enter="change">
              </div></td>
              <td>
                <div class="input-group">
                  <input
                    v-model="phone_number"
                    type="text"
                    class="form-control col-xs-2"
                    placeholder=""
                    @keyup.enter="change">
                </div>
              </td><td>
              <div class="input-group"/></td>
            </tr>
            <tr
              v-for="admin in admins"
              :key="admin.id">
              <td>{{ admin.username }}</td>
              <td>{{ admin.phone_number }}</td>
              <button
                type="button"
                class="row inner-btn btn-sm"
                @click="jump(admin.id)"
              >详情</button>
            </tr>
          </tbody>
        </table>
      </div>
      <Pagination
        :rows="rows"
        :perpage="per_limit"
        @change="changePage"/>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import Pagination from '../../components/pagination'
import axios from 'axios'
import Alert from '../../components/alert'
export default {
  name: 'AdminManagement',
  components: {Alert, Pagination, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        active: true
      }],
      admins: [],
      username: '',
      phone_number: '',
      page: 1,
      rows: 0,
      per_limit: 8,
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      query_id: -1,
      test_add_admin: false
    }
  },
  created: function () {
    axios.get('http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-list/', {
      params: {
        username: '',
        phone_number: '',
        page_limit: this.per_limit,
        page: 1
      }
    }).then(
      response => {
        this.rows = response.data.count
        let _admins = []
        for (let data of response.data.content) {
          _admins.push({'id': data['admin_id'], 'username': data['username'], 'phone_number': data['phone_number']})
        }
        this.admins = _admins
      }).catch(
      error => {
        this.error_message = '读取数据出错' + error
        this.wrong_count_down = 5
      }
    )
  },
  methods: {
    jump: function (id) {
      if (id === -1) {
        this.test_add_admin = true
        this.$router.push({name: 'AddAdmin'})
      } else {
        this.query_id = id
        this.$router.push({name: 'AdminDetail', query: {'admin_id': this.query_id}})
      }
    },
    change: function () {
      axios.get('http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-list/', {
        params: {
          username: this.username,
          phone_number: this.phone_number,
          page_limit: this.per_limit,
          page: this.page
        }
      }).then(
        response => {
          this.rows = response.data.count
          let _admins = []
          for (let data of response.data.content) {
            _admins.push({
              'id': data['admin_id'],
              'username': data['username'],
              'phone_number': data['phone_number']
            })
          }
          this.admins = _admins
        }).catch(
        error => {
          this.error_message = '读取数据出错' + error.response.data.message
          this.wrong_count_down = 5
        }
      )
    },
    changePage: function (currentpage) {
      this.page = currentpage
      this.change()
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  #head-btn {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .inner-btn {
    margin-top: 2%;
    margin-left: 38%;
  }

  .table-div {
    text-align: center;
  }

  .table {
    border: 1px solid #d3d9df;
  }

  th {
    min-width: 100px;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  #head-btn,
  .inner-btn {
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  #head-btn:hover,
  .inner-btn:hover,
  #head-btn:active,
  .inner-btn:active {
    background-color: #5e0057;
  }

</style>
