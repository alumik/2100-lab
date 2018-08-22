<!--suppress ALL -->
<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>课程详情</h2>
      {{ error_message }}
      <div>
        <div class="head-btn">
          <button
            type="button"
            class="row btn btn-sm my-in-btn"
            @click="jump(1)"
          >修改课程</button>
        </div>
        <div class="head-btn">
          <button
            v-b-modal.delete
            type="button"
            class="row btn btn-sm my-in-btn"
          >删除课程</button>
        </div>
        <ConfirmModal
          id="delete"
          title="确认删除"
          text="您确定要删除该课程吗？"
          @click="deleteMessage"/>
      </div>
      <div>
        <table
          class="table table-striped table-hover"
          width="100%">
          <tbody>
            <tr>
              <td class="head-td">
                课程代码
              </td>
              <td class="content-td">
                {{ course.codename }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                课程名
              </td>
              <td class="content-td">
                {{ course.title }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                阅后即焚时间
              </td>
              <td class="content-td">
                {{ course.expire_duration }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                价格
              </td>
              <td class="content-td">
                {{ course.price }}
              </td>
            </tr>            <tr>
              <td class="head-td">
                分销金比例
              </td>
              <td class="content-td">
                {{ course.reward_percent }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                添加时间
              </td>
              <td class="content-td">
                {{ course.created_at }}
              </td>
            </tr>
            <tr>
              <td class="head-td">
                修改时间
              </td>
              <td class="content-td">
                {{ course.updated_at }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="my-intro">
        <h3 class="text-left">课程简介</h3>
        <h2 class="text-left">{{ course.description }}</h2>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import ConfirmModal from '../components/ConfirmModal'
import axios from 'axios'
export default {
  name: 'BackendCourseDetail',
  components: {ConfirmModal, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: this.$route.query.course_id.toString(),
        active: true
      }],
      test_router: -1,
      error_message: '',
      course: {
        'codename': '',
        'name': '',
        'time': '',
        'price': '',
        'reward_percent': '',
        'created_at': '',
        'updated_at': '',
        'description': ''
      }
    }
  },
  created: function () {
    axios.get('http://localhost:8000/api/v1/courses/backstage/course-management/get-course-detail', {
      params: {
        course_id: this.$route.query.course_id
      }
    }).then(
      response => {
        this.course.codename = response.data.codename
        this.course.title = response.data.title
        this.course.expire_duration = response.data.expire_duration.replace('P', '').replace('DT', '天').replace('H', '小时').replace('M', '分钟').replace('S', '秒钟')
        this.course.price = response.data.price
        this.course.reward_percent = response.data.reward_percent
        this.course.created_at = response.data.created_at.replace('T', ' ').substring(0, 19)
        this.course.updated_at = response.data.updated_at.replace('T', ' ').substring(0, 19)
        this.course.description = response.data.description
      }).catch(
      error => {
        this.error_message = '读取数据出错' + error.response.data.message
      }
    )
  },
  methods: {
    jump: function (id) {
      this.test_router = id
      this.$router.push({name: 'EditCourse', query: {'course_id': this.$route.query.course_id}})
    },
    deleteMessage: function () {
      axios.get('http://localhost:8000/api/v1/courses/backstage/course-management/get-course-detail')
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .head-btn {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .my-in-btn {
    margin-right: auto;
    margin-left: 50px;
  }

  .head-td {
    width: 35%;
  }

  .content-td {
    width: 65%;
  }

  .table {
    border: 1px solid #d3d9df;
  }

  .btn {
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .btn:active {
    background-color: #5e0057;
  }
</style>
