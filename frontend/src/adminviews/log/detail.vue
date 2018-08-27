<template>
  <Basic :items="items">
    <div class="body">
      <h1>日志列表</h1>
      <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
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
              <td class="sm-td">{{ compute_date(log.created_at) }}</td>
              <td class="md-td">{{ compute_admin_name(log.admin_username) }}</td>
              <td class="lg-td">{{ log.message }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <Pagination
        :rows="rows"
        :perpage="per_page"
        @change="change_page"/>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import Pagination from '../../components/pagination'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'LogDetail',
  components: { Alert, Pagination, Basic },
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '日志查询',
          href: '/admin/log'
        },
        {
          text: '日志列表',
          active: true
        }
      ],
      titles: [{ label: '时间' }, { label: '管理员名称' }, { label: '内容' }],
      logs: [],
      rows: 20,
      page: 1,
      per_page: 10,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      select: [],
      num_pages: 0
    }
  },
  created () {
    let temp = this.$route.query.select.split(',')
    for (let i = 0; i < temp.length; i++) {
      if (temp[i] !== '') {
        this.select.push(parseInt(temp[i]))
      }
    }
    const that = this
    axios
      .get(
        'http://localhost:8000/api/v1/admin/backstage/log-management/get-admin-log/',
        {
          params: {
            page_limit: that.per_page,
            page: that.page,
            admin_username: that.$route.query.admin_username,
            start_timestamp: that.$route.query.begin_date,
            end_timestamp: that.$route.query.end_date,
            filters: that.select
          },
          paramsSerializer: function (params) {
            return qs.stringify(params, { arrayFormat: 'repeat' })
          }
        }
      )
      .then(function (response) {
        that.logs = response.data.content
        that.rows = response.data.count
        if (response.data.num_pages === 0) {
          that.num_pages = 1
        } else {
          that.num_pages = response.data.num_pages
        }
      })
      .catch(function (error) {
        that.wrong = '查询日志失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    change_page: function (page) {
      this.page = page
      const that = this
      axios
        .get(
          'http://localhost:8000/api/v1/admin/backstage/log-management/get-admin-log/',
          {
            params: {
              page_limit: that.per_page,
              page: that.page,
              admin_username: that.$route.query.admin_username,
              start_timestamp: that.$route.query.begin_date,
              end_timestamp: that.$route.query.end_date,
              filters: that.select
            },
            paramsSerializer: function (params) {
              return qs.stringify(params, { arrayFormat: 'repeat' })
            }
          }
        )
        .then(function (response) {
          that.logs = response.data.content
          that.rows = response.data.count
          if (response.data.num_pages === 0) {
            that.num_pages = 1
          } else {
            that.num_pages = response.data.num_pages
          }
        })
        .catch(function (error) {
          that.wrong = '查询日志失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    compute_date: function (date) {
      let temp = new Date(date)
      return temp.toLocaleString()
    },
    compute_admin_name: function (name) {
      let index = name.search('_deleted_')
      if (index !== -1) {
        return name.slice(0, index) + '\n' + '（已删除）'
      } else {
        return name
      }
    }
  }
}
</script>

<style scoped>
.body {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1,
h6 {
  padding-left: 15px;
  margin: 25px 0;
  color: #204269;
  text-align: left;
}

h6 {
  margin-bottom: 15px;
  font-weight: bold;
}

.table-div {
  padding-right: 15px;
  padding-left: 15px;
  overflow-x: scroll;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

td {
  font-size: 1rem;
  vertical-align: middle;
}

thead tr {
  font-weight: bold;
  color: #999;
}

.sm-td {
  width: 200px;
}

.md-td {
  width: 250px;
}

.lg-td {
  width: 400px;
}
</style>
