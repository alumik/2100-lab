<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>数据分析</h1>
        </div>
      </div>
      <Alert
        id="alert"
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <b-tabs
        class="data"
        @input="change_tab">
        <b-tab title="总体概况"/>
        <b-tab
          title="时间对比"
          active>
          <div class="tab-content">
            <div class="search">
              <div class="col-md-2">
                <div>开始时间</div>
                <date-picker
                  v-model="begin_date"
                  :config="options"
                  class="date-picker"/>
              </div>
              <div class="col-md-2">
                <div>结束时间</div>
                <date-picker
                  v-model="end_date"
                  :config="options"
                  class="date-picker"/>
              </div>
              <div class="col-md-3">
                <div>步长</div>
                <div class="step">
                  <b-input-group
                    append="月">
                    <b-form-input v-model="month"/>
                  </b-input-group>
                  <b-input-group
                    append="日">
                    <b-form-input v-model="day"/>
                  </b-input-group>
                </div>
              </div>
              <div class="col-md-2">
                <div class="search-button">
                  <b-button
                    id="search"
                    variant="outline-secondary"
                    @click="search">
                    查询
                  </b-button>
                </div>
              </div>
            </div>
            <div class="charts">
              <div class="users">
                <h5>新增用户数</h5>
                <ve-line
                  :data="charts_users"
                  :colors="colors1">
                  <div
                    v-show="data_empty"
                    class="data-empty">请输入查询条件</div>
                </ve-line>
              </div>
              <div class="money">
                <h5>销售额</h5>
                <ve-line
                  :data="charts_money"
                  :settings="money_settings"
                  :colors="colors2">
                  <div
                    v-show="data_empty"
                    class="data-empty">请输入查询条件</div>
                </ve-line>
              </div>
              <div class="courses">
                <h5>新增课程数</h5>
                <ve-histogram
                  :data="charts_courses"
                  :colors="colors1">
                  <div
                    v-show="data_empty"
                    class="data-empty">请输入查询条件</div>
                </ve-histogram>
              </div>
              <div class="courses">
                <h5>新增订单数</h5>
                <ve-histogram
                  :data="charts_orders"
                  :colors="colors2">
                  <div
                    v-show="data_empty"
                    class="data-empty">请输入查询条件</div>
                </ve-histogram>
              </div>
            </div>
          </div>
        </b-tab>
      </b-tabs>
    </div>
  </Basic>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/bread_crumb'
import Basic from '../basic/basic'
import axios from 'axios'
import Alert from '../../components/alert'
export default {
  name: 'TimeData',
  components: { Alert, Basic, BreadCrumb, Menu, AdminNavbar },
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '数据分析',
          active: true
        }
      ],
      colors1: ['#cd4c46'],
      colors2: ['#5b9bd1'],
      end_date: new Date(),
      begin_date: new Date(new Date().getTime() - 24 * 60 * 60 * 1000),
      options: {
        format: 'YYYY/MM/DD',
        useCurrent: true
      },
      month: '',
      day: '',
      charts_users: {
        columns: ['日期', '新增用户数'],
        rows: []
      },
      charts_money: {
        columns: ['日期', '新增销售额'],
        rows: []
      },
      money_settings: { area: true },
      charts_courses: {
        columns: ['日期', '新增课程数'],
        rows: []
      },
      charts_orders: {
        columns: ['日期', '新增订单数'],
        rows: []
      },
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      data_empty: true
    }
  },
  methods: {
    change_tab: function (val) {
      if (val === 0) {
        this.$router.push('/admin/data/total')
      }
    },
    get_step: function () {
      if (this.day === '' && this.month === '') {
        return -1
      }
      let month = this.month === '' ? 0 : parseFloat(this.month)
      let day = this.day === '' ? 0 : parseFloat(this.day)
      if (
        (this.day !== '' && day % 1 !== 0) ||
        (this.month !== '' && month % 1 !== 0)
      ) {
        return -2
      } else {
        return 30 * month + day
      }
    },
    get_start_end_time: function () {
      let start = Date.parse(this.begin_date) / 1000
      let end = Date.parse(this.end_date) / 1000
      if (start >= end) {
        return -1
      } else {
        let temp = []
        temp[0] = start
        temp[1] = end
        return temp
      }
    },
    check_date: function () {
      let step = this.get_step()
      if (step === -1 || step === 0) {
        this.wrong = '您所输入的时间有误'
        this.wrong_count_down = this.dismiss_second
        return -1
      } else if (step === -2) {
        this.wrong = '请输入整数'
        this.wrong_count_down = this.dismiss_second
        return -1
      }
      let time = this.get_start_end_time()
      if (time === -1 || step * 24 * 60 * 60 - 1 > time[1] - time[0]) {
        this.wrong = '您所输入的时间有误'
        this.wrong_count_down = this.dismiss_second
        return -1
      }
      let temp = []
      temp[0] = time[0]
      temp[1] = time[1]
      temp[2] = step
      return temp
    },
    get_data: function (val) {
      this.charts_users.rows = []
      this.charts_money.rows = []
      this.charts_courses.rows = []
      this.charts_orders.rows = []
      for (let i = val.length - 1; i >= 0; i--) {
        this.charts_users.rows.push({
          日期: val[i].right_time.slice(0, 10),
          新增用户数: val[i].data.customers_count
        })
        this.charts_money.rows.push({
          日期: val[i].right_time.slice(0, 10),
          新增销售额: val[i].data.income
        })
        this.charts_courses.rows.push({
          日期: val[i].right_time.slice(0, 10),
          新增课程数: val[i].data.courses_count
        })
        this.charts_orders.rows.push({
          日期: val[i].right_time.slice(0, 10),
          新增订单数: val[i].data.orders_count
        })
      }
    },
    search: function () {
      const that = this
      let data = this.check_date()
      if (data === -1) {
        return null
      } else {
        axios
          .get(
            'http://localhost/api/v1/data/data-management/get-data-by-time/',
            {
              params: {
                start_timestamp: data[0],
                end_timestamp: data[1],
                time_step: data[2]
              }
            }
          )
          .then(function (response) {
            that.get_data(response.data.content)
            that.data_empty = false
          })
          .catch(function (error) {
            that.wrong = '获取信息失败！' + error
            that.wrong_count_down = that.dismiss_second
          })
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

.tab-content {
  text-align: left;
}

.charts {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-top: 100px;
}

.charts > div {
  flex-basis: 50%;
  justify-content: space-around;
  text-align: center;
}

h5 {
  font-weight: bold;
  text-align: center;
}

p {
  text-align: center;
}

.data {
  margin: 0 15px;
}

h1 {
  color: #204269;
  text-align: left;
}

.search {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  padding-top: 30px;
  padding-bottom: 30px;
  margin-bottom: 50px;
  border-bottom: 1px solid #ced4da;
}

.col-md-2 > div,
.col-md-2 > .date-picker {
  width: 150px;
  height: 38px;
  text-align: center;
  vertical-align: middle;
}

.col-md-3 > div {
  z-index: 1;
  width: 250px;
  height: 38px;
  text-align: center;
  vertical-align: middle;
}

.input-group > .form-control:focus {
  z-index: 1;
}

.step {
  display: flex;
}

.search-button {
  padding-top: 38px;
}

#search {
  height: 38px;
  color: white;
  background-color: #337ab7;
  border: 1px solid #d3d9df;
  box-shadow: none !important;
}

#search:hover {
  background-color: #286090;
}

.data-empty {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #888;
  background-color: rgba(255, 255, 255, 0.7);
}

.head-title {
  display: flex;
  margin: 25px 0;
}

.head-container {
  padding: 0 15px;
  margin-bottom: 15px;
  text-align: left;
}
</style>
