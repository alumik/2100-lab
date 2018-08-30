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
                class="time-btn"
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
              </div>
              <div class="statistics2">
                <div class="number">
                  <h5>{{ sale }}</h5>
                  <p>销售额</p>
                </div>
              </div>
              <div class="statistics3">
                <div class="number">
                  <h5>{{ increased_courses }}</h5>
                  <p>新增课程数</p>
                </div>
              </div>
              <div class="statistics4">
                <div class="number">
                  <h5>{{ orders }}</h5>
                  <p>订单数</p>
                </div>
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
        <b-tab title="时间对比"/>
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
  name: 'TotalData',
  components: { Alert, Basic, BreadCrumb, Menu, AdminNavbar },
  /**
   * @returns {{
   * items: *[], 面包屑路由地址
   * buttons: *[], 数据时段选择按钮
   * increased_users: number, 新增用户数
   * sale: number, 新增销售额
   * increased_courses: number, 新增课程数
   * orders: number, 新增订单数
   * colors1: Array,
   * colors2: Array,
   * 图表颜色
   * praise_top: object,
   * study_top: object,
   * 图表数据
   * praise_top_setting: object,
   * study_top_setting: object,
   * 图表设置
   * dismiss_second: number,
   * wrong_count_down: number,
   * wrong: string
   * Alert组件所需参数
   * }}
   */
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
      colors1: ['#5b9bd1'],
      colors2: ['#cd4c46'],
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
          title: '课程名',
          up_votes: '点赞数'
        }
      },
      study_top_setting: {
        labelMap: {
          title: '课程名',
          learners: '学习人数'
        }
      },
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  /**
   * 该函数初始化数据分析总体分析页面，
   * 向后端通过get方法发送所需数据距今天数，
   * 获取后端发送的相关数据，
   * 进行错误捕捉并进行提示信息。
   */
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
    axios
      .get('http://localhost/api/v1/data/data-management/get-overall-data/', {
        params: { days: days }
      })
      .then(function (response) {
        that.increased_users = response.data.customers_count
        that.sale = response.data.income
        that.increased_courses = response.data.courses_count
        that.orders = response.data.orders_count
        that.praise_top.rows = response.data.top_up_voted_courses
        that.study_top.rows = response.data.top_learned_courses
      })
      .catch(function (error) {
        if (error.response.data.message === 'Access denied.') {
          that.wrong = '您没有权限获取数据！'
          that.wrong_count_down = that.dismiss_second
        } else {
          that.wrong = '获取数据失败！'
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数实现数据分析页面tab跳转，
     * 接收标识标签的参数，
     * 判断不为当前标签页则跳转。
     * @param val
     */
    change_tab: function (val) {
      if (val === 1) {
        this.$router.push('/admin/data/time')
      }
    },
    /**
     * 该函数根据页面上按钮组的选择，
     * 返回表示所需数据距今天数的Number类型常量
     * @returns {number}
     */
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
    /**
     * 该函数获取数据，
     * 向后端通过get方法发送所需数据距今天数，
     * 获取后端发送的相关数据，
     * 进行错误捕捉并进行提示信息。
     */
    search: function () {
      const that = this
      let days = this.get_days()
      axios
        .get('http://localhost/api/v1/data/data-management/get-overall-data/', {
          params: { days: days }
        })
        .then(function (response) {
          that.increased_users = response.data.customers_count
          that.sale = response.data.income
          that.increased_courses = response.data.courses_count
          that.orders = response.data.orders_count
          that.praise_top.rows = response.data.top_up_voted_courses
          that.study_top.rows = response.data.top_learned_courses
        })
        .catch(function (error) {
          if (error.response.data.message === 'Access denied.') {
            that.wrong = '您没有权限获取数据！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.wrong = '获取数据失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
    },
    /**
     * 该函数改变所选按钮状态，
     * 接收一个表示当前选中按钮下标的参数，
     * 根据所选参数改变按钮状态，
     * 执行获取数据操作，刷新页面数据。
     * @param val
     */
    change_button_state: function (val) {
      for (let i = 0; i < this.buttons.length; i++) {
        if (i === val) {
          this.buttons[i].state = true
        } else {
          this.buttons[i].state = false
        }
      }
      this.search()
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

h1 {
  color: #204269;
  text-align: left;
}

.tab-content {
  text-align: left;
}

.statistics {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  margin: 50px -10px;
}

.statistics > div {
  display: flex;
  flex: 1 1 180px;
  justify-content: center;
  height: 100px;
  padding: 20px;
  margin: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

@media (max-width: 600px) {
  .statistics {
    flex-wrap: wrap;
  }

  .statistics > div {
    flex: 1 1 500px;
  }
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

.col-md-2 > div {
  width: 150px;
  height: 31px;
  text-align: center;
  vertical-align: middle;
}

.title {
  margin-top: 25px;
}

.time-btn,
.time-btn:not(:disabled) {
  margin-right: 5px;
  color: #204269;
  background-color: transparent;
  border: none;
  border-radius: 5px !important;
  box-shadow: none !important;
}

.time-btn:not(:disabled).active,
.time-btn:hover,
.time-btn:focus {
  color: white;
  background-color: #5b9bd1 !important;
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
