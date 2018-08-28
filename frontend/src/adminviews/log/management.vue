<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <h1>日志查询</h1>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <div class="table-div">
        <table class="table">
          <thead>
            <tr>
              <th>管理员名称</th>
              <th>开始时间</th>
              <th>结束时间</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input
                  id="admin"
                  v-model="admin_id"
                  type="text"
                  class="form-control">
              </td>
              <td>
                <div class="col-md-6">
                  <date-picker
                    v-model="begin_date"
                    :config="options"/>
                </div>
              </td>
              <td>
                <div class="col-md-6">
                  <date-picker
                    v-model="end_date"
                    :config="options"/>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h4>查询项目</h4>
      <form class="checkbox-div">
        <b-form-group class="outer">
          <b-form-checkbox
            :indeterminate="indeterminate"
            aria-describedby="options1"
            aria-controls="options1"
            @change="toggle_all">
            全选
          </b-form-checkbox>
        </b-form-group>
        <div class="checkbox">
          <b-form-group class="inner">
            <b-form-checkbox-group
              id="row1"
              v-model="select1"
              :options="options1"
              name="row1"
              stacked/>
          </b-form-group>
          <b-form-group class="inner">
            <b-form-checkbox-group
              id="row2"
              v-model="select2"
              :options="options2"
              name="row2"
              stacked/>
          </b-form-group>
          <b-form-group class="inner">
            <b-form-checkbox-group
              id="row3"
              v-model="select3"
              :options="options3"
              name="row3"
              stacked/>
          </b-form-group>
          <b-form-group class="inner">
            <b-form-checkbox-group
              id="row4"
              v-model="select4"
              :options="options4"
              name="row4"
              stacked/>
          </b-form-group>
        </div>
      </form>
      <div class="button-group">
        <button
          type="submit"
          class="btn"
          @click="to_detail">查询</button>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import Alert from '../../components/alert'
export default {
  name: 'LogManagement',
  components: { Alert, Basic },
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '日志查询',
          active: true
        }
      ],
      begin_date: new Date(new Date().getTime() - 24 * 60 * 60 * 1000),
      end_date: new Date(),
      options: {
        format: 'YYYY/MM/DD'
      },
      admin_id: '',
      select1: [],
      options1: [
        { text: '增加管理员', value: 1 },
        { text: '修改管理员权限', value: 2 },
        { text: '修改管理员名称', value: 3 },
        { text: '修改管理员密码', value: 4 }
      ],
      select2: [],
      options2: [
        { text: '删除管理员', value: 5 },
        { text: '订单退款', value: 6 },
        { text: '删除用户', value: 7 },
        { text: '禁言用户', value: 8 }
      ],
      select3: [],
      options3: [
        { text: '解除禁言', value: 9 },
        { text: '认证用户', value: 10 },
        { text: '取消认证', value: 11 },
        { text: '删除留言', value: 12 }
      ],
      select4: [],
      options4: [
        { text: '回复留言', value: 13 },
        { text: '增加课程', value: 14 },
        { text: '修改课程', value: 15 },
        { text: '删除课程', value: 16 }
      ],
      page_jump: false,
      wrong: '',
      wrong_count_down: 0,
      dismiss_second: 5
    }
  },
  computed: {
    indeterminate: function () {
      if (
        this.select1.length === 4 &&
        this.select2.length === 4 &&
        this.select3.length === 4 &&
        this.select4.length === 4
      ) {
        return false
      } else if (
        this.select1.length === 0 &&
        this.select2.length === 0 &&
        this.select3.length === 0 &&
        this.select4.length === 0
      ) {
        return false
      } else {
        return true
      }
    }
  },
  methods: {
    to_detail: function () {
      let begin_date = Date.parse(this.begin_date) / 1000
      let end_date = Date.parse(this.end_date) / 1000
      if (begin_date > end_date) {
        this.wrong = '您输入的查询日期有误！'
        this.wrong_count_down = this.dismiss_second
      } else {
        this.page_jump = true
        this.$router.push({
          name: 'LogDetail',
          query: {
            admin_username: this.admin_id,
            begin_date: begin_date,
            end_date: end_date,
            select:
              this.select1 +
              ',' +
              this.select2 +
              ',' +
              this.select3 +
              ',' +
              this.select4
          }
        })
      }
    },
    toggle_all (checked) {
      if (checked) {
        this.select1 = []
        this.select2 = []
        this.select3 = []
        this.select4 = []
        for (let i = 0; i < 4; i++) {
          this.select1.push(this.options1[i].value)
          this.select2.push(this.options2[i].value)
          this.select3.push(this.options3[i].value)
          this.select4.push(this.options4[i].value)
        }
      } else {
        this.select1 = []
        this.select2 = []
        this.select3 = []
        this.select4 = []
      }
    }
  }
}
</script>

<style scoped>
.body {
  padding: 20px;
  margin: 70px 20px 20px;
  overflow-x: auto;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1,
h4 {
  padding-left: 15px;
  margin: 25px 0;
  color: #204269;
  text-align: left;
}

.table-div {
  padding-left: 15px;
}

table {
  width: 400px;
  text-align: center;
}

input {
  width: 178px;
}

.col-md-6 {
  align-items: center;
}

tr {
  align-items: center;
}

tr td {
  width: 180px;
}

.checkbox-div {
  padding-left: 20px;
  text-align: left;
}

.outer {
  font-size: 1.2em;
  font-weight: normal;
}

.checkbox {
  display: flex;
}

.inner {
  padding-left: 30px;
}

.button-group {
  display: flex;
  justify-content: flex-start;
  padding-top: 10px;
  padding-left: 20px;
}

.btn {
  margin-right: 2px;
  margin-left: 2px;
  color: white;
  background-color: #337ab7;
  border: 1px solid #d3d9df;
  outline: none;
}

.btn:hover,
.btn:active {
  background-color: #286090;
}
</style>
