<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <h1>数据分析</h1>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <b-tabs
        class="data"
        @input="change_tab">
        <b-tab
          title="总体概况"
          active>
          <div class="tab-content">
            <b-button-group
              class="title">
              <b-button
                v-for="btn in buttons"
                :key="btn.id"
                :pressed.sync="btn.state"
                variant="outline-secondary"
                @click="change_button_state(btn.id)">
                {{ btn.text }}
              </b-button>
            </b-button-group>
            <div class="statistics">
              <div class="statistics1">
                <div class="number">
                  <h5>{{ increased_users }}</h5>
                  <p>新增用户数</p>
                </div>
                <img
                  class="image"
                  src="../../assets/logo.png">
              </div>
              <div class="statistics2">
                <div class="number">
                  <h5>{{ sale }}</h5>
                  <p>销售额</p>
                </div>
                <img
                  class="image"
                  src="../../assets/logo.png">
              </div>
              <div class="statistics3">
                <div class="number">
                  <h5>{{ increased_courses }}</h5>
                  <p>新增课程数</p>
                </div>
                <img
                  class="image"
                  src="../../assets/logo.png">
              </div>
              <div class="statistics4">
                <div class="number">
                  <h5>{{ orders }}</h5>
                  <p>订单数</p>
                </div>
                <img
                  class="image"
                  src="../../assets/logo.png">
              </div>
            </div>
            <div class="charts">
              <div id="charts-praise_top">
                <h5>课程点赞数TOP5</h5>
                <ve-histogram
                  :data="praise_top"
                  :colors="colors1"
                  :settings="praise_top_setting"/>
              </div>
              <div id="charts_learners_top">
                <h5>学习人数TOP5</h5>
                <ve-histogram
                  :data="study_top"
                  :colors="colors2"
                  :settings="study_top_setting"/>
              </div>
            </div>
          </div>
        </b-tab>
        <b-tab title="时间对比" >
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
                    @click="search2">
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
                  :colors="colors1"/>
              </div>
              <div class="money">
                <h5>销售额</h5>
                <ve-line
                  :data="charts_users"
                  :settings="money_settings"
                  :colors="colors2"/>
              </div>
              <div class="courses">
                <h5>新增课程数</h5>
                <ve-histogram
                  :data="charts_courses"
                  :colors="colors1"/>
              </div>
              <div class="courses">
                <h5>新增学习人数</h5>
                <ve-histogram
                  :data="charts_learners"
                  :colors="colors2"/>
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
  name: 'Data',
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
      buttons: [
        { id: 0, state: true, text: '今天' },
        { id: 1, state: false, text: '近一周' },
        { id: 2, state: false, text: '近一月' },
        { id: 3, state: false, text: '近半年' }
      ],
      increased_users: 0,
      sale: 0,
      increased_courses: 0,
      orders: 0,
      colors1: ['#ff5722'],
      colors2: ['#448aff'],
      praise_top: {
        columns: ['title', 'up_votes'],
        rows: []
      },
      study_top: {
        columns: ['title', 'learners'],
        rows: []
      },
      praise_top_setting: {
        labelMap: {
          'title': '课程名',
          'up_votes': '点赞数'
        }
      },
      study_top_setting: {
        labelMap: {
          'title': '课程名',
          'learners': '学习人数'
        }
      },
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
        rows: [
          { '日期': '2018-08-01', '新增用户数': 1500 },
          { '日期': '2018-08-02', '新增用户数': 1300 },
          { '日期': '2018-08-03', '新增用户数': 1200 },
          { '日期': '2018-08-04', '新增用户数': 1000 },
          { '日期': '2018-08-05', '新增用户数': 800 }
        ]
      },
      charts_money: {
        columns: ['日期', '销售额'],
        rows: [
          { '日期': '2018-08-01', '销售额': 1500 },
          { '日期': '2018-08-02', '销售额': 1300 },
          { '日期': '2018-08-03', '销售额': 1200 },
          { '日期': '2018-08-04', '销售额': 1000 },
          { '日期': '2018-08-05', '销售额': 800 }
        ]
      },
      money_settings: { area: true },
      charts_courses: {
        columns: ['日期', '新增课程数'],
        rows: [
          { '日期': '2018-08-01', '新增课程数': 1500 },
          { '日期': '2018-08-02', '新增课程数': 1300 },
          { '日期': '2018-08-03', '新增课程数': 1200 },
          { '日期': '2018-08-04', '新增课程数': 1000 },
          { '日期': '2018-08-05', '新增课程数': 800 }
        ]
      },
      charts_learners: {
        columns: ['日期', '新增学习人数'],
        rows: [
          { '日期': '2018-08-01', '新增学习人数': 1500 },
          { '日期': '2018-08-02', '新增学习人数': 1300 },
          { '日期': '2018-08-03', '新增学习人数': 1200 },
          { '日期': '2018-08-04', '新增学习人数': 1000 },
          { '日期': '2018-08-05', '新增学习人数': 800 }
        ]
      },
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  created () {
    const that = this
    let i
    for (i = 0; i < that.buttons.length; i++) {
      if (that.buttons[i].state) {
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
    axios.get('http://localhost:8000/api/v1/data/data-management/get-overall-data/',
      {params: {days: days}})
      .then(function (response) {
        that.increased_users = response.data.customers_count
        that.sale = response.data.income
        that.increased_courses = response.data.courses_count
        that.orders = response.data.orders_count
        that.praise_top.rows = response.data.top_up_voted_courses
        that.study_top.rows = response.data.top_learned_courses
      })
      .catch(function (error) {
        that.wrong = '获取数据失败' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    change_tab: function (val) {
      // console.log(val)
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
    search1: function () {
      const that = this
      let days = this.get_days()
      axios.get('http://localhost:8000/api/v1/data/data-management/get-overall-data/',
        {params: {days: days}})
        .then(function (response) {
          if (response.data.message === 'Access denied.') {
            that.wrong = '您没有权限获取数据！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.increased_users = response.data.customers_count
            that.sale = response.data.income
            that.increased_courses = response.data.courses_count
            that.orders = response.data.orders_count
            that.praise_top.rows = response.data.top_up_voted_courses
            that.study_top.rows = response.data.top_learned_courses
          }
        })
        .catch(function (error) {
          that.wrong = '获取数据失败' + error
          that.wrong_count_down = that.dismiss_second
        })
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
    search2: function () {
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
            // console.log(response.data.content)
          })
          .catch(function (error) {
            that.wrong = '获取信息失败！' + error
            that.wrong_count_down = that.dismiss_second
          })
      }
    },
    change_button_state: function (val) {
      for (let i = 0; i < this.buttons.length; i++) {
        if (i === val) {
          this.buttons[i].state = true
        } else {
          this.buttons[i].state = false
        }
      }
      this.search1()
    }
  }
}
</script>

<style scoped>
  .my-basic {
    min-width: 800px;
  }

  .tab-content {
    padding: 20px;
    text-align: left;
  }

  .statistics {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .statistics > div {
    display: flex;
    justify-content: space-between;
    width: 300px;
    height: 100px;
    padding: 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    border: 1px solid #ced4da;
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

  .image {
    width: 50px;
    height: 50px;
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
</style>
