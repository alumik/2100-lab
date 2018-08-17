<template>
  <div>
    <AdminNavbar id="navbar"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="study">
        <BreadCrumb :items="items"/>
        <h1>相关课程</h1>
        <div class="table_div">
          <table
            id="study_table"
            class="table table-striped">
            <thead>
              <tr>
                <td
                  v-for="title in titles"
                  :key="title.id">
                  {{ title.label }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="log in logs"
                :key="log.id">
                <td>{{ log.course_code }}</td>
                <td>{{ log.course_name }}</td>
                <td>{{ log.progress }}</td>
                <td>{{ log.time }}</td>
                <td>{{ log.state }}</td>
              </tr>
            </tbody>
          </table>
          <Pagination :rows="rows"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
export default {
  name: 'Course',
  components: {Menu, AdminNavbar, BreadCrumb, Pagination},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: '用户详情',
        href: '/admin/user/detail'
      }, {
        text: '相关课程',
        active: true
      }],
      titles: [
        { label: '课程代码' },
        { label: '课程名' },
        { label: '学习进度' },
        { label: '最近学习时间' },
        { label: '是否焚毁' }
      ],
      logs: [
        { course_code: 'SOFT1', course_name: '计算机', progress: '01:22', time: '2018-08-14', state: '已焚毁' },
        { course_code: 'ENGLISH3', course_name: '英语写作', progress: '15:00', time: '2018-05-14', state: '未焚毁' },
        { course_code: 'PHYSICS5', course_name: '小孔成像', progress: '16:00', time: '2018-06-20', state: '已焚毁' }
      ],
      rows: 10
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 1000px;
  }

  h1 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1000px;
  }

  #study {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
    text-align: center;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }
</style>
