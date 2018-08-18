<template>
  <div class="html">
    <AdminNavbar id="navbar"/>
    <div id="body">
      <div>
        <Menu class="menu"/>
      </div>
      <div id="date">
        <BreadCrumb :items="items"/>
        <h1>数据分析</h1>
        <div class="date-div">
          <button @click="change_type">切换图表的类型</button>
          <ve-chart
            :data="date1"
            :settings="settings1"/>
          <ve-line :data="date2"/>
          <ve-histogram :data="date1"/>
          <ve-histogram
            :data="date2"
            :settings="settings2"/>
          <ve-bar :data="date2"/>
          <ve-pie :data="date1"/>
          <ve-scatter :data="date2"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'Date',
  components: {BreadCrumb, Menu, AdminNavbar},
  data () {
    this.type = ['line', 'histogram']
    this.index = 1
    this.settings2 = {
      showLine: ['课程1购买量']
    }
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '数据分析',
        active: true
      }],
      date1: {
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
      date2: {
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
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 800px;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 800px;
    height: calc(100% - 70px);
  }

  .menu {
    position: fixed;
  }

  #date {
    flex-basis: 100%;
    padding: 0;
    margin-left: 200px;
  }

  .date-div {
    padding-right: 15px;
    padding-left: 15px;
  }
</style>
