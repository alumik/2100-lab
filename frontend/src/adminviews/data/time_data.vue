<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <h1>数据分析</h1>
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
              <div class="col-md-2">
                <div>步长</div>
                <div class="step">
                  <b-input-group
                    size="sm"
                    append="月">
                    <b-form-input v-model="month"/>
                  </b-input-group>
                  <b-input-group
                    size="sm"
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
import BreadCrumb from '../../components/breadCrumb'
import Basic from '../basic/basic'
import axios from 'axios'
import Alert from '../../components/alert'
export default {
  name: 'TimeData',
  components: {Alert, Basic, BreadCrumb, Menu, AdminNavbar},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '数据分析',
        active: true
      }],
      colors1: ['#ff5722'],
      colors2: ['#448aff'],
      begin_date: new Date(),
      end_date: new Date(),
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
    get_days: function () {
      let i
      for (i = 0; i < this.buttons.length; i++) {
        if (this.buttons[i].state) {
          break
        }
      }
      let days = 1
      if (i === 0) {
        days = 1
      } else if (i === 1) {
        days = 7
      } else if (i === 2) {
        days = 31
      } else if (i === 3) {
        days = 182
      }
      return days
    },
    get_step: function () {
      if (this.day === '' && this.month === '') {
        return -1
      }
      let month = (this.month === '') ? 0 : parseFloat(this.month)
      let day = (this.day === '') ? 0 : parseFloat(this.day)
      if ((this.day !== '' && day % 1 !== 0) ||
          (this.month !== '' && month % 1 !== 0)) {
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
      if (time === -1 ||
          (step * 24 * 60 * 60) > (time[1] - time[0])) {
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
        this.charts_users.rows.push(
          {
            日期: val[i].right_time.slice(0, 10),
            新增用户数: val[i].data.customers_count
          }
        )
        this.charts_money.rows.push(
          {
            日期: val[i].right_time.slice(0, 10),
            新增销售额: val[i].data.income
          }
        )
        this.charts_courses.rows.push(
          {
            日期: val[i].right_time.slice(0, 10),
            新增课程数: val[i].data.courses_count
          }
        )
        this.charts_orders.rows.push(
          {
            日期: val[i].right_time.slice(0, 10),
            新增订单数: val[i].data.orders_count
          }
        )
      }
    },
    search: function () {
      const that = this
      let data = this.check_date()
      if (data === -1) {
        return null
      } else {
        axios.get('http://localhost:8000/api/v1/data/data-management/get-data-by-time/',
          {
            params: {
              start_timestamp: data[0],
              end_timestamp: data[1],
              time_step: data[2]
            }
          })
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
    overflow-x: scroll;
  }

  .tab-content {
    padding: 20px;
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
    margin-right: 20px;
    margin-left: 20px;
    border: 1px solid #f3f5ee;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .search {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    padding-top: 10px;
    padding-bottom: 10px;
    border-top: 1px solid #ced4da;
    border-bottom: 1px solid #ced4da;
  }

  .col-md-2 > div,
  .col-md-2 > .date-picker {
    width: 150px;
    height: 31px;
    text-align: center;
    vertical-align: middle;
  }

  .step {
    display: flex;
  }

  .tab-content > div {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .search-button {
    padding-top: 30px;
  }

  #search {
    height: 30px;
    font-size: 0.8em;
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
</style>
