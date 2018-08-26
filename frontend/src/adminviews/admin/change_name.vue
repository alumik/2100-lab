<template>
  <Basic :items="items">
    <div class="my-content">
      <h1>修改管理员名</h1>
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
      <div>
        <div class="form-group">
          <h4
            class="form-check-label"
            for="newname">原管理员名：{{ old_name }}</h4>
        </div>
        <div class="form-group">
          <label
            class="form-check-label"
            for="newname">新管理员名</label>
          <input
            id="newname"
            v-model="new_name"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <a
          id="save-btn"
          class="btn"
          @click="submit_message">
          <simple-line-icons
            id="add-icon"
            icon="pin"
            color="white"
            class="icon"/>
          保存
        </a>
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
  name: 'ChangeName',
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
          text: '修改管理员名',
          active: true
        }
      ],
      new_name: null,
      old_name: null,
      wrong_count_down: 0,
      success_count_down: 0,
      error_message: ''
    }
  },
  created () {
    axios
      .get(
        'http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/',
        {
          params: {
            admin_id: this.$route.query.admin_id
          }
        }
      )
      .then(response => {
        this.old_name = response.data.username
      })
      .catch(error => {
        this.error_message = '读取数据出错' + error.response.data.message
        this.wrong_count_down = 5
      })
  },
  methods: {
    submit_message: function () {
      if (this.new_name === null) {
        this.error_message = '请输入新名字'
        this.wrong_count_down = 5
      } else if (this.old_name === this.new_name) {
        this.error_message = '新旧名字一致'
        this.wrong_count_down = 5
      } else {
        axios
          .post(
            'http://localhost:8000/api/v1/admin/backstage/admin-management/change-admin-username/',
            qs.stringify({
              admin_id: this.$route.query.admin_id,
              new_username: this.new_name
            })
          )
          .then(response => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = response.data.new_username
            setTimeout(this.router_push, 3000)
          })
          .catch(error => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = error.response.message
            this.wrong_count_down = 5
          })
      }
    },
    router_push () {
      this.$router.push({
        name: 'AdminDetail',
        query: { admin_id: this.$route.query.admin_id }
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

label {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
}

.form-group {
  margin-top: 60px;
  margin-left: 15px;
}

#save-btn {
  color: white;
}

.btn {
  margin-top: 40px;
  margin-right: 3px;
  margin-left: 15px;
  color: white;
  text-align: right;
  background-color: #449c44;
  border: 1px solid #d3d9df;
}

.btn:hover,
.btn:active {
  background-color: #4db14d;
}
</style>
