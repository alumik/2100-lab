<!--suppress ALL -->
<template>
  <Basic :items="items">
    <div class="my-content">
      <div>
        <h1>分配权限</h1>
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
        <h4 class="my-text">管理员账号：{{ admin_id }}</h4>
        <div>
          <h4 class="my-text">权限选择：</h4>
          <b-form-group class="my-form-group">
            <b-form-checkbox
              v-model="all_selected"
              aria-controls="flavours"
              @change="toggle_all"
            >
              <h4>{{ all_selected ? '取消全选' : '全选' }}</h4>
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
            <a
              id="save-btn"
              class="btn"
              @click="submit_message">
              <simple-line-icons
                id="add-icon"
                icon="user-follow"
                color="white"
                class="icon"/>
              保存
            </a>
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
import Alert from '../../components/alert'
export default {
  name: 'DistributeAuthority',
  components: { Alert, Basic },
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
          href:
            '/admin/adminmanagement/detail?admin_id=' +
            this.$route.query.admin_id.toString()
        },
        {
          text: '分配权限',
          active: true
        }
      ],
      admin_id: '',
      flavours: [
        '评论管理权限',
        '课程管理权限',
        '客户管理权限',
        '日志管理权限',
        '订单管理权限'
      ],
      selected: [],
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      all_selected: false,
      test_router: false
    }
  },
  watch: {
    selected () {
      if (
        this.all_selected === true &&
        this.selected.length !== this.flavours.length
      ) {
        this.all_selected = false
      }
      if (
        this.all_selected === false &&
        this.selected.length === this.flavours.length
      ) {
        this.all_selected = true
      }
    }
  },
  mounted () {
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
        for (let permission of response.data.admin_groups) {
          this.selected.push(this.transfer_permission(permission))
        }
      })
      .catch(error => {
        this.error_message = '读取数据出错' + error.response.data.message
        this.wrong_count_down = 5
      })
  },
  methods: {
    toggle_all (checked) {
      this.selected = checked ? this.flavours.slice() : []
    },
    transfer_permission (permission) {
      switch (permission) {
        case 'comment_admin':
          return '评论管理权限'
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
    reverse_permission (sel) {
      switch (sel) {
        case '评论管理权限':
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
    submit_message () {
      let adminGroups = []
      for (let sel of this.selected) {
        adminGroups.push(this.reverse_permission(sel))
      }
      axios
        .post(
          'http://localhost:8000/api/v1/admin/backstage/admin-management/change-admin-groups/',
          qs.stringify(
            {
              new_admin_groups: adminGroups,
              admin_id: this.admin_id
            },
            { arrayFormat: 'repeat' }
          )
        )
        .then(response => {
          this.error_message = response.data.message
          this.$router.push({
            name: 'AdminDetail',
            query: { admin_id: this.admin_id }
          })
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
  margin: 25px 15px;
  color: #204269;
  text-align: left;
}

.my-form-group {
  margin-top: 40px;
  margin-left: 15px;
}

.my-text {
  margin-top: 50px;
  margin-left: 15px;
}

#save-btn {
  color: white;
}

.btn {
  margin-top: 250px;
  margin-right: 3px;
  margin-left: 3px;
  color: white;
  text-align: right;
  background-color: #0c0;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #090;
}
</style>
