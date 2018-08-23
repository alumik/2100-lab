<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>修改管理员名</h2>
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
          <label
            class="form-check-label"
            for="newname">原管理员名：{{ old_name }}</label>
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
        <button
          class="btn btn-sm"
          @click="submitMessage"
        >保存</button>
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
  components: {Alert, Basic},
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
        text: '修改管理员名',
        active: true
      }],
      new_name: null,
      old_name: null,
      wrong_count_down: 0,
      success_count_down: 0,
      error_message: ''
    }
  },
  created () {
    axios.get('http://localhost:8000/api/v1/admin/backstage/admin-management/get-admin-detail/', {
      params: {
        admin_id: this.$route.query.admin_id
      }
    }).then(
      response => {
        this.old_name = response.data.username
      }
    ).catch(
      error => {
        this.error_message = '读取数据出错' + error.response.data.message
        this.wrong_count_down = 5
      }
    )
  },
  methods: {
    submitMessage: function () {
      if (this.new_name === null) {
        this.error_message = '请输入新名字'
        this.wrong_count_down = 5
      } else if (this.old_name === this.new_name) {
        this.error_message = '新旧名字一致'
        this.wrong_count_down = 5
      } else {
        axios.post('http://localhost:8000/api/v1/admin/backstage/admin-management/change-admin-username/', qs.stringify({
          admin_id: this.$route.query.admin_id,
          new_username: this.new_name
        })).then(
          response => {
            this.error_message = response.data.new_username
            this.$router.push({name: 'AdminDetail', query: {'admin_id': this.$route.query.admin_id}})
          }
        ).catch(
          error => {
            this.error_message = error.response.message
            this.wrong_count_down = 5
          }
        )
      }
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .form-group {
    margin-top: 60px;
  }

  .btn {
    margin-top: 25px;
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
