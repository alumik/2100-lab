<template>
  <div class="html">
    <AdminNavbar id="navbar"/>
    <div id="body">
      <Menu/>
      <div id="detail">
        <BreadCrumb :items="items"/>
        <h1>日志列表</h1>
        <div class="table_div">
          <table class="table table-striped">
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
                <td class="sm_td">{{ log.time }}</td>
                <td class="sm_td">{{ log.account }}</td>
                <td class="lg_td">{{ log.content }}</td>
              </tr>
            </tbody>
          </table>
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
  name: 'LogDetail',
  components: {BreadCrumb, Menu, AdminNavbar},
  data () {
    return {
      items: [{
        text: '首页',
        href: '/admin'
      }, {
        text: '日志查询',
        href: '/admin/log'
      }, {
        text: '日志列表',
        active: true
      }],
      titles: [
        { label: '时间' },
        { label: '管理员账号' },
        { label: '内容' }
      ],
      logs: [
        { time: '2018-08-15 14:15:28', account: '1001', content: '1001删除了ID为3的留言' },
        { time: '2018-08-15 15:20:10', account: '1010', content: '1010回复了ID为4的留言' },
        { time: '2018-08-17 18:15:25', account: '1025', content: '1025删除了ID为5的留言' }
      ]
    }
  }
}
</script>

<style scoped>
  .html {
    height: 100%;
  }

  #navbar {
    min-width: 800px;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 800px;
    height: calc(100% - 70px);
  }

  #detail {
    flex-basis: 100%;
    padding: 0;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  table {
    font-size: 1.2em;
    border: 1px solid #d3d9df;
  }

  td {
    vertical-align: middle;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .sm_td {
    width: 150px;
  }

  .lg_td {
    width: 400px;
  }
</style>
