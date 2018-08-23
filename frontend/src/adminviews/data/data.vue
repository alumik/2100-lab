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
          <div class="tab1-content">
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
            <div class="table">
              <div id="table1">
                <h5>课程点赞数TOP5</h5>
                <ve-histogram
                  :data="praise_top"
                  :colors="colors1"/>
              </div>
              <div id="table2">
                <h5>学习点赞数TOP5</h5>
                <ve-histogram
                  :data="study_top"
                  :colors="colors2"/>
              </div>
            </div>
          </div>
        </b-tab>
        <b-tab title="时间对比" >
          <br>I'm the second tab content
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
    this.type = ['line', 'histogram']
    this.index = 1
    this.settings2 = {
      showLine: ['课程1购买量']
    }
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
      data1: {
        columns: ['日期', '购买量'],
        rows: [
          {'日期': '1月1日', '购买量': 123},
          {'日期': '1月2日', '购买量': 1223},
          {'日期': '1月3日', '购买量': 2123},
          {'日期': '1月4日', '购买量': 4123},
          {'日期': '1月5日', '购买量': 3123},
          {'日期': '1月6日', '购买量': 7123}
        ]
      },
      settings1: {type: this.type[this.index]},
      data2: {
        columns: ['日期', '课程1购买量', '课程2购买量'],
        rows: [
          {'日期': '8月13日', '课程1购买量': 1350, '课程2购买量': 1455},
          {'日期': '8月14日', '课程1购买量': 1200, '课程2购买量': 1105},
          {'日期': '8月15日', '课程1购买量': 1000, '课程2购买量': 900}
        ]
      }
    }
  },
  methods: {
    change_type: function () {
      if (this.index === 0) {
        this.index = 1
      } else {
        this.index = 0
      }
      this.settings1 = {type: this.type[this.index]}
    },
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

  .tab1-content {
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

  .table {
    display: flex;
    justify-content: space-around;
    margin-top: 70px;
  }

  .table > div {
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
</style>
