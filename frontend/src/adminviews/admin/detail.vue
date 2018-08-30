<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="head-container">
        <div class="head-title">
          <h1>管理员详情</h1>
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
          <div class="button-group">
            <a
              id="distribution-btn"
              class="btn"
              @click="jump(1)">
              <simple-line-icons
                icon="plus"
                color="white"
                class="icon"/>
              分配权限
            </a>
            <a
              id="change-password-btn"
              class="btn"
              @click="jump(2)">
              <simple-line-icons
                icon="note"
                color="white"
                class="icon"/>
              修改密码
            </a>
            <a
              id="change-username-btn"
              class="btn"
              @click="jump(3)">
              <simple-line-icons
                icon="tag"
                color="white"
                class="icon"/>
              修改管理员名
            </a>
            <a
              id="delete-user-btn"
              class="btn"
              @click="show_delete_modal">
              <simple-line-icons
                icon="exclamation"
                color="white"
                class="icon"/>
              删除管理员
            </a>
          </div>
        </div>
      </div>
      <b-modal
        id="modal"
        ref="modal"
        title="确认删除"
        ok-title="确认"
        cancel-title="取消"
        centered
        @ok="click_ok">
        <p>您确定要删除该管理员吗？</p>
      </b-modal>
      <div class="table-div">
        <table
          class="table"
          width="100%">
          <tbody>
            <tr>
              <td class="head-td">
                管理员名称
              </td>
              <td class="content-td">
                {{ admin.username }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                管理员手机号
              </td>
              <td class="content-td">
                {{ admin.phone_number }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                添加时间
              </td>
              <td class="content-td">
                {{ admin.date_joined }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                修改时间
              </td>
              <td class="content-td">
                {{ admin.updated_at }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                权限
              </td>
              <td class="content-td">
                {{ admin.admin_groups }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import ConfirmModal from '../components/confirm_modal'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'AdminDetail',
  components: { Alert, ConfirmModal, Basic },
  /**
   * @returns {{
   * items: *[], 路由跳转信息
   * admin: {
   * admin_id: string, 用户ID，数据库自增数据段
   * username: string, 用户名，默认为手机号
   * phone_number: string, 用户手机号
   * date_joined: string, 用户加入时间
   * updated_at: string, 用户最近登录时间
   * admin_groups: string 用户权限组
   * },
   * admin_id: number, 当前访问用户ID
   * error_message: string, 错误信息提示
   * wrong_count_down: number, 错误信息倒计时
   * success_count_down: number, 正确信息倒计时
   * test_router: number 路由跳转信息
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
          href: '/admin/adminmanagement'
        },
        {
          text: this.$route.query.admin_id.toString(),
          active: true
        }
      ],
      admin: {
        admin_id: '',
        username: '',
        phone_number: '',
        date_joined: '',
        updated_at: '',
        admin_groups: ''
      },
      admin_id: -1,
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      test_router: -1
    }
  },
  /**
   * 将路由ID存储到访问用户ID中
   * 发送请求，访问用户ID
   * 得到回应，调用数据初始化函数获取当前用户信息
   * 得到错误，调用信息转换函数显示五秒
   */
  created () {
    this.admin_id = this.$route.query.admin_id
    axios
      .get(
        'http://localhost/api/v1/admin/backstage/admin-management/get-admin-detail/',
        {
          params: {
            admin_id: this.admin_id
          }
        }
      )
      .then(response => {
        this.initial_data(response)
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
     * 错误信息转换函数
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
     * 用户信息生成函数
     * @param response
     * 权限管理注意超级管理员权限的显示
     */
    initial_data (response) {
      this.admin.admin_id = response.data.admin_id
      this.admin.username = response.data.username
      this.admin.phone_number = response.data.phone_number
      this.admin.date_joined = response.data.date_joined
        .replace('T', ' ')
        .substring(0, 19)
      this.admin.updated_at = response.data.updated_at
        .replace('T', ' ')
        .substring(0, 19)
      for (let permission of response.data.admin_groups) {
        if (permission === 'super_admin') {
          this.admin.admin_groups = '超级管理员权限'
          break
        } else {
          if (this.admin.admin_groups === '') {
            this.admin.admin_groups = this.transfer_permission(permission)
          } else {
            this.admin.admin_groups =
              this.admin.admin_groups +
              '，' +
              this.transfer_permission(permission)
          }
        }
      }
    },
    /**
     * 权限英中转换的函数
     * @param permission
     * @returns {string}
     */
    transfer_permission (permission) {
      switch (permission) {
        case 'comment_admin':
          return '留言管理权限'
        case 'course_admin':
          return '课程管理权限'
        case 'customer_admin':
          return '用户管理权限'
        case 'log_admin':
          return '日志管理权限'
        case 'order_admin':
          return '订单管理权限'
        case 'super_admin':
          return '超级管理员权限'
      }
    },
    /**
     * 路由跳转函数：分配权限页面、更改密码页面、更改用户名页面
     * @param id
     */
    jump: function (id) {
      if (id === 1) {
        this.test_router = 1
        this.$router.push({
          name: 'DistributeAuthority',
          query: { admin_id: this.admin_id }
        })
      } else if (id === 2) {
        this.test_router = 2
        this.$router.push({
          name: 'ChangeCode',
          query: { admin_id: this.admin_id }
        })
      } else if (id === 3) {
        this.test_router = 3
        this.$router.push({
          name: 'ChangeName',
          query: { admin_id: this.admin_id }
        })
      }
    },
    /**
     * 显示删除模态框
     */
    show_delete_modal () {
      this.$refs.modal.show()
    },
    /**
     * 删除模态框提交键点击后提交请求函数
     * 得到回应，展示删除成功信息
     * 得到错误，展示错误信息
     */
    click_ok: function () {
      this.$refs.modal.hide()
      axios
        .post(
          'http://localhost/api/v1/admin/backstage/admin-management/delete-admin/',
          qs.stringify({
            admin_id: this.admin_id
          })
        )
        .then(response => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = '删除成功！'
          this.$router.push({ name: 'AdminManagement' })
        })
        .catch(error => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = this.init_error_message(error.response.data.message)
          this.wrong_count_down = 5
        })
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  text-align: left;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #204269;
  text-align: left;
}

.head-td {
  width: 35%;
  font-weight: bold;
  color: #337ab7;
  background-color: #f3f4f6;
}

.content-td {
  width: 65%;
  color: #748085;
}

.table-div {
  padding-right: 15px;
  padding-left: 15px;
  text-align: center;
}

.table td {
  vertical-align: middle;
}

.button-group {
  display: inline-block;
  float: right;
}

#distribution-btn {
  color: white;
  background-color: #337ab7;
}

#distribution-btn:hover {
  background-color: #286090;
}

#change-password-btn {
  color: white;
  background-color: #337ab7;
}

#change-password-btn:hover {
  background-color: #286090;
}

#change-username-btn {
  color: white;
  background-color: #337ab7;
}

#change-username-btn:hover {
  background-color: #286090;
}

#delete-user-btn {
  color: white;
  background-color: #dd514c;
}

#delete-user-btn:hover {
  background-color: #ba2d28;
}

.btn {
  margin-left: 3px;
  color: white;
  text-align: right;
  background-color: #4db14d;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #449c44;
}

.head-title {
  display: flex;
  flex-wrap: wrap;
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
