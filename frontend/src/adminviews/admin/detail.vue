<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="head-container">
        <div class="head-title">
          <h1>管理员详情</h1>
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
          class="table table-striped"
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
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import ConfirmModal from '../components/ConfirmModal'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'AdminDetail',
  components: { Alert, ConfirmModal, Basic },
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
  created () {
    this.admin_id = this.$route.query.admin_id
    axios
      .get(
        'http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/',
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
        this.error_message = '读取数据出错' + error.response.data.message
        this.wrong_count_down = 5
      })
  },
  methods: {
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
              ',' +
              this.transfer_permission(permission)
          }
        }
      }
    },
    transfer_permission (permission) {
      switch (permission) {
        case 'comment_admin':
          return '用户评论管理权限'
        case 'course_admin':
          return '课程管理权限'
        case 'customer_admin':
          return '客户管理权限'
        case 'log_admin':
          return '日志权限'
        case 'order_admin':
          return '订单管理权限'
        case 'super_admin':
          return '超级管理员权限'
      }
    },
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
    show_delete_modal () {
      this.$refs.modal.show()
    },
    click_ok: function () {
      this.$refs.modal.hide()
      axios
        .post(
          'http://localhost:8000/api/v1/admin/backstage/admin-management/delete-admin/',
          qs.stringify({
            admin_id: this.admin_id
          })
        )
        .then(response => {
          this.$router.push({ name: 'AdminManagement' })
        })
        .catch(error => {
          this.error_message = error.response.message
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
}

.content-td {
  width: 65%;
}

.table-div {
  padding-right: 15px;
  padding-left: 15px;
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
