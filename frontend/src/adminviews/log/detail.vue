<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>日志列表</h1>
        </div>
        <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      </div>
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
  /**
   * @returns {{
   * items: *[], 面包屑路由地址
   * titles: Array, 日志列表标题
   * logs: Array, 日志列表数据
   * select: Array, 所选日志项目
   * rows: number, 数据总条数
   * page: number, 当前页数
   * per_page: number, 单页数据条数
   * num_pages: number, 数据总页数
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
      select: [],
      rows: 0,
      page: 1,
      per_page: 15,
      num_pages: 0,
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  /**
   * 该函数在初始化日志界面时调用，
   * 将表示选择项目的字符串转化为字符串，
   * 通过get方法向后端发送单页最大数据量，当前页数，用户名称，开始结束时间戳及选择项目的数据，
   * 获得后端发送的日志信息，
   * 并捕捉错误进行信息提示。
   */
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
        'http://localhost/api/v1/admin/backstage/log-management/get-admin-log/',
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
        if (error) {
          that.wrong = '查询日志失败！' + error
          that.wrong_count_down = that.dismiss_second
        }
      })
  },
  methods: {
    /**
     * 该函数接受表示页数的参数，
     * 修改当前页数，并进行查询操作。
     * @param page
     */
    change_page: function (page) {
      this.page = page
      const that = this
      axios
        .get(
          'http://localhost/api/v1/admin/backstage/log-management/get-admin-log/',
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
          if (error) {
            that.wrong = '查询日志失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
    },
    /**
     * 该函数接受一个表示日期的字符串，
     * 将UTC时间转化为当地时间，
     * 并返回转换后的字符串
     * @param date
     * @returns {string}
     */
    compute_date: function (date) {
      let temp = new Date(date)
      return temp.toLocaleString()
    },
    /**
     * 该函数接受一个表示管理员名称的字符串参数，
     * 并通过是否被删除进行转换，
     * 返回转换后的管理员名称的字符串参数。
     * @param name
     * @returns {*}
     */
    compute_admin_name: function (name) {
      let index = name.search('_deleted_')
      if (index !== -1) {
        return name.slice(0, index) + '（已删除）'
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
  color: #204269;
  text-align: left;
}

h6 {
  font-weight: bold;
}

.table-div {
  padding: 0 15px;
  margin-bottom: 25px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

.table td {
  font-size: 1rem;
  vertical-align: middle;
}

.table thead tr {
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
