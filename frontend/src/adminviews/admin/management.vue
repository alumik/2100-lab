<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="head-container">
        <div class="head-title">
          <h1>管理员列表</h1>
          <a
            id="head-btn"
            class="btn"
            @click="jump(-1)">
            <simple-line-icons
              id="add-icon"
              icon="user-follow"
              color="white"
              class="icon"/>
            新增管理员
          </a>
        </div>
        <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      </div>
      <div class="table-div">
        <table class="table table-striped">
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
                    class="form-control my-in-input"
                    placeholder=""
                    @keyup.enter="change">
              </div></td>
              <td>
                <div class="input-group">
                  <input
                    v-model="phone_number"
                    type="text"
                    class="form-control my-in-input"
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
              <td class="buttons">
                <a
                  id="detail-button"
                  class="btn"
                  @click="jump(admin.id)">
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
        :perpage="per_limit"
        @change="change_page"/>
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
  components: { Alert, Pagination, Basic },
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '管理员管理',
          active: true
        }
      ],
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
      test_router: false,
      num_pages: 0
    }
  },
  created: function () {
    axios
      .get(
        'http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-list/',
        {
          params: {
            username: '',
            phone_number: '',
            page_limit: this.per_limit,
            page: 1
          }
        }
      )
      .then(response => {
        this.rows = response.data.count
        this.num_pages = this.update_num_pages(response.data.num_pages)
        let _admins = []
        for (let data of response.data.content) {
          _admins.push({
            id: data['admin_id'],
            username: data['username'],
            phone_number: data['phone_number']
          })
        }
        this.admins = _admins
      })
      .catch(error => {
        this.error_message = '读取数据出错' + error
        this.wrong_count_down = 5
      })
  },
  methods: {
    jump: function (id) {
      if (id === -1) {
        this.test_router = true
        this.$router.push({ name: 'AddAdmin' })
      } else {
        this.query_id = id
        this.$router.push({
          name: 'AdminDetail',
          query: { admin_id: this.query_id }
        })
      }
    },
    change: function () {
      axios
        .get(
          'http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-list/',
          {
            params: {
              username: this.username,
              phone_number: this.phone_number,
              page_limit: this.per_limit,
              page: this.page
            }
          }
        )
        .then(response => {
          this.rows = response.data.count
          this.num_pages = this.update_num_pages(response.data.num_pages)
          let _admins = []
          for (let data of response.data.content) {
            _admins.push({
              id: data['admin_id'],
              username: data['username'],
              phone_number: data['phone_number']
            })
          }
          this.admins = _admins
        })
        .catch(error => {
          this.error_message = '读取数据出错' + error.response.data.message
          this.wrong_count_down = 5
        })
    },
    change_page: function (currentpage) {
      this.page = currentpage
      this.change()
    },
    update_num_pages: function (page) {
      if (page === 0) {
        return 1
      } else {
        return page
      }
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

#head-btn {
  display: inline-block;
  color: white;
  text-align: right;
  background-color: #4db14d;
}

#head-btn:hover,
#head-btn:active {
  background-color: #449c44;
}

#add-icon {
  margin-top: 3px;
}

.my-in-input {
  width: 50px;
  margin-right: 10%;
  margin-left: 10%;
}

.btn {
  margin-right: 3px;
  margin-left: 3px;
  border: 1px solid #d3d9df;
}

#detail-button {
  color: #5b9bd1;
}

.btn:hover,
.btn:active {
  background-color: rgba(91, 155, 209, 0.2);
}

.table-div {
  padding: 0 15px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

td {
  vertical-align: middle;
}

h1,
h6 {
  color: #204269;
}

h1 {
  text-align: left;
}

h6 {
  margin-bottom: 0;
  font-weight: bold;
}

th {
  min-width: 100px;
}

thead tr {
  font-weight: bold;
  color: #999;
}

.head-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 25px 0;
}

.head-container {
  padding: 0 15px;
  margin-bottom: 15px;
  text-align: left;
}
</style>
