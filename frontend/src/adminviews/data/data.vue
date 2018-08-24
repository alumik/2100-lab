<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <h1>数据分析</h1>
      <b-tabs class="data">
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
                  :colors="colors1"/>
              </div>
              <div id="charts_learners_top">
                <h5>学习人数TOP5</h5>
                <ve-histogram
                  :data="study_top"
                  :colors="colors2"/>
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
                    <b-form-input/>
                  </b-input-group>
                  <b-input-group
                    size="sm"
                    append="日">
                    <b-form-input/>
                  </b-input-group>
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
export default {
  name: 'Data',
  components: {Basic, BreadCrumb, Menu, AdminNavbar},
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
        { id: 1, state: false, text: '昨天' },
        { id: 2, state: false, text: '近一周' },
        { id: 3, state: false, text: '近一月' }
      ],
      increased_users: 1500,
      sale: 150000,
      increased_courses: 100,
      orders: 1000,
      colors1: ['#ff5722'],
      colors2: ['#448aff'],
      praise_top: {
        columns: ['课程名', '点赞数'],
        rows: [
          { '课程名': '数学', '点赞数': 1500 },
          { '课程名': '语文', '点赞数': 1300 },
          { '课程名': '英语', '点赞数': 1200 },
          { '课程名': '物理', '点赞数': 1000 },
          { '课程名': '化学', '点赞数': 800 }
        ]
      },
      study_top: {
        columns: ['课程名', '学习人数'],
        rows: [
          { '课程名': '数学', '学习人数': 1500 },
          { '课程名': '语文', '学习人数': 1300 },
          { '课程名': '英语', '学习人数': 1200 },
          { '课程名': '物理', '学习人数': 1000 },
          { '课程名': '化学', '学习人数': 800 }
        ]
      },
      begin_date: new Date(),
      end_date: new Date(),
      options: {
        format: 'YYYY/MM/DD',
        useCurrent: true
      },
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
      }
    }
  },
  methods: {
    change_button_state: function (val) {
      for (let i = 0; i < this.buttons.length; i++) {
        if (i === val) {
          this.buttons[i].state = true
        } else {
          this.buttons[i].state = false
        }
      }
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
    justify-content: space-between;
    margin-top: 20px;
  }

  .statistics > div {
    display: flex;
    justify-content: space-between;
    width: 300px;
    height: 100px;
    padding: 20px;
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
    vertical-align: top;
  }

  .step {
    display: flex;
  }

  .tab-content > div {
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
