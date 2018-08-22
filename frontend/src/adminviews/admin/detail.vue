<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>管理员详情</h2>
      {{ error_message }}
      <div class="button_group">
        <button
          type="button"
          class="row btn btn-sm"
          @click="jump(1)"
        >分配权限</button>
        <button
          type="button"
          class="row btn btn-sm"
          @click="jump(2)"
        >修改密码</button>
        <button
          type="button"
          class="row btn btn-sm"
          @click="jump(3)"
        >修改管理员名</button>
        <button
          v-b-modal.delete
          type="button"
          class="row btn btn-sm"
        >删除管理员</button>
        <ConfirmModal
          id="delete"
          title="确认删除"
          text="您确定要删除该管理员吗？"
          @click="deleteMessage"/>
      </div>
      <div class="table_div">
        <table
          class="table table-striped table-hover"
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
import ConfirmModal from '../components/ConfirmModal'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'AdminDetail',
  components: {ConfirmModal, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: this.$route.query.admin_id.toString(),
        active: true
      }],
      admin: {
        'admin_id': '',
        'username': '',
        'phone_number': '',
        'date_joined': '',
        'updated_at': '',
        'admin_groups': ''
      },
      admin_id: -1,
      error_message: '',
      test_router: -1
    }
  },
  created () {
    this.admin_id = this.$route.query.admin_id
    axios.get('http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/', {
      params: {
        admin_id: this.admin_id
      }
    }).then(
      response => {
        this.admin.admin_id = response.data.admin_id
        this.admin.username = response.data.username
        this.admin.phone_number = response.data.phone_number
        this.admin.date_joined = response.data.date_joined.replace('T', ' ').substring(0, 19)
        this.admin.updated_at = response.data.updated_at.replace('T', ' ').substring(0, 19)
        for (let permission of response.data.admin_groups) {
          this.admin_groups += permission
        }
      }).catch(
      error => {
        this.error_message = '读取数据出错' + error.response.data.message
      }
    )
  },
  methods: {
    jump: function (id) {
      if (id === 1) {
        this.test_router = 1
        this.$router.push({name: 'DistributeAuthority', query: {admin_id: this.admin_id}})
      } else if (id === 2) {
        this.test_router = 2
        this.$router.push({name: 'ChangeCode', query: {admin_id: this.admin_id}})
      } else if (id === 3) {
        this.test_router = 3
        this.$router.push({name: 'ChangeName', query: {admin_id: this.admin_id}})
      }
    },
    deleteMessage: function () {
      axios.post('http://localhost:8000/api/v1/admin/backstage/admin-management/delete-admin/',
        qs.stringify({
          admin_id: this.admin_id
        })).then(
        response => {
          this.$router.push({name: 'AdminManagement'})
        }).catch(
        error => {
          this.error_message = error.response.message
        }
      )
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .head-td {
    width: 35%;
  }

  .content-td {
    width: 65%;
  }

  .button_group {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .btn {
    margin-right: 25px;
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
</style>
