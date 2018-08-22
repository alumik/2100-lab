<!--suppress ALL -->
<template>
  <Basic :items="items">
    <div class="my-content">
      <div>
        <h2>分配权限</h2>
        {{ error_message }}
        <h4 class="my-text">管理员账号：{{ admin_id }}</h4>
        <div>
          <h4 class="my-text">权限选择：</h4>
          <b-form-group class="my-form-group">
            <b-form-checkbox
              v-model="allSelected"
              aria-controls="flavours"
              @change="toggleAll"
            >
              <h4>{{ allSelected ? '取消全选' : '全选' }}</h4>
            </b-form-checkbox>
            <b-form-checkbox-group
              id="flavors"
              v-model="selected"
              :options="flavours"
              stacked
              size="lg"
              name="flavs"
              class="ml-4"
              aria-label="Individual flavours"
            />
            <b-button
              class="btn"
              @click="submitMessage"
            >提交</b-button>
          </b-form-group>
        </div>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'DistributeAuthority',
  components: {Basic},
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
        href: '/admin/adminmanagement/detail?admin_id=' + this.$route.query.admin_id.toString()
      }, {
        text: '分配权限',
        active: true
      }],
      admin_id: '',
      flavours: ['用户评论管理权限', '课程管理权限', '客户管理权限', '日志管理权限', '订单管理权限'],
      selected: [],
      error_message: '',
      allSelected: false
    }
  },
  watch: {
    selected () {
      if (this.allSelected === true && this.selected.length !== this.flavours.length) {
        this.allSelected = false
      }
      if (this.allSelected === false && this.selected.length === this.flavours.length) {
        this.allSelected = true
      }
    }
  },
  mounted () {
    this.admin_id = this.$route.query.admin_id
    axios.get('http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/', {
      params: {
        admin_id: this.admin_id
      }
    }).then(
      response => {
        for (let permission of response.data.admin_groups) {
          this.selected.push(this.transferPermission(permission))
        }
      }).catch(
      error => {
        this.error_message = '读取数据出错' + error.response.data.message
      })
  },
  methods: {
    toggleAll (checked) {
      this.selected = checked ? this.flavours.slice() : []
    },
    transferPermission (permission) {
      switch (permission) {
        case 'comment_admin':
          return '用户评论管理权限'
        case 'course_admin':
          return '课程管理权限'
        case 'customer_admin':
          return '客户管理权限'
        case 'log_admin':
          return '日志管理权限'
        case 'order_admin':
          return '订单管理权限'
      }
    },
    reversePermission (sel) {
      switch (sel) {
        case '用户评论管理权限':
          return 'comment_admin'
        case '课程管理权限':
          return 'course_admin'
        case '客户管理权限':
          return 'customer_admin'
        case '日志管理权限':
          return 'log_admin'
        case '订单管理权限':
          return 'order_admin'
      }
    },
    submitMessage () {
      let adminGroups = []
      for (let sel of this.selected) {
        adminGroups.push(this.reversePermission(sel))
      }
      axios.post('http://localhost:8000/api/v1/admin/backstage/admin-management/change-admin-groups/',
        qs.stringify({
          new_admin_groups: adminGroups,
          admin_id: this.admin_id
        }, {arrayFormat: 'repeat'})).then(
        response => {
          this.error_message = response.data.message
          this.$router.push({name: 'AdminDetail', query: {'admin_id': this.admin_id}})
        }
      ).catch(
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

  .my-form-group {
    margin-top: 40px;
  }

  .my-text {
    margin-top: 50px;
  }

  .btn {
    margin-top: 250px;
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
