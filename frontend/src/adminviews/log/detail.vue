<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>日志列表</h1>
      <div class="table-div">
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
              <td class="sm-td">{{ log.time }}</td>
              <td class="sm-td">{{ log.account }}</td>
              <td class="lg-td">{{ log.content }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
export default {
  name: 'LogDetail',
  components: { Basic },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
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
  .my-basic {
    min-width: 800px;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table-div {
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

  .sm-td {
    width: 150px;
  }

  .lg-td {
    width: 400px;
  }
</style>
