<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="head-container">
        <div class="head-title">
          <h1>管理员列表</h1>
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
                <div class="input-group-sm my-input">
                  <input
                    v-model="username"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="change">
              </div></td>
              <td>
                <div class="input-group-sm my-input">
                  <input
                    v-model="phone_number"
                    type="text"
                    class="form-control"
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
  /**
   * @returns {{
   * items: *[], 路由信息
   * admins: Array, 管理员信息
   * username: string, 查询的用户名信息
   * phone_number: string, 查询的用户手机号信息
   * page: number, 页码信息
   * rows: number, 总计记录数量信息
   * per_limit: number, 每页记录数量
   * error_message: string, 错误信息
   * wrong_count_down: number, 错误信息显示时间
   * success_count_down: number, 成功信息显示时间
   * query_id: number, 想要查询的管理员的ID
   * test_router: boolean, 路由测试信息
   * num_pages: number 总共页数信息
   * }}
   */
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
      per_limit: 15,
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      query_id: -1,
      test_router: false,
      num_pages: 0
    }
  },
  /**
   * 页面初始化，发送请求得到当前管理员列表信息
   * 发送查询条件：用户名+用户手机号+每页限制数量+页码数
   * 得到回应，保存记录信息
   * 得到错误，显示错误信息五秒
   */
  created: function () {
    axios
      .get(
        'http://localhost/api/v1/admin/backstage/admin-management/get-admin-list/',
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
        this.wrong_count_down = 0
        this.success_count_down = 0
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
        this.wrong_count_down = 0
        this.success_count_down = 0
        this.error_message = this.init_error_message(error.response.data.message)
        this.wrong_count_down = 5
      })
  },
  methods: {
    /**
     * 路由跳转函数，目标是管理员详细信息界面
     * @param id
     */
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
    /**
     * 具体条件查询函数
     * 根据用户输入的具体查询条件来执行查询操作
     * 得到回应，存储和显示查询到的信息
     * 得到错误，显示五秒错误信息
     */
    change: function () {
      axios
        .get(
          'http://localhost/api/v1/admin/backstage/admin-management/get-admin-list/',
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
          this.error_message = this.init_error_message(error.response.data.message)
          this.wrong_count_down = 5
        })
    },
    /**
     * 生成错误信息
     * @param message
     * @returns {string}
     */
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        default:
          return '数据库查询出错'
      }
    },
    /**
     * 换页函数
     * @param currentpage
     */
    change_page: function (currentpage) {
      this.page = currentpage
      this.change()
    },
    /**
     * 更新页码函数
     * @param page
     * @returns {*}
     */
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

.my-input {
  display: inline-block;
  max-width: 200px;
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
  margin-bottom: 25px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

.table td {
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
