<!--suppress ALL -->
<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="title">
        <h1>课程详情</h1>
        <Alert
          :count_down="wrong_count_down"
          :instruction="error_message"
          variant="danger"
          @decrease="wrong_count_down-1"
          @zero="wrong_count_down=0"/>
        <Alert
          :count_down="success_count_down"
          :instruction="error_message"
          variant="success"
          @decrease="success_count_down-1"
          @zero="success_count_down=0"/>
        <div>
          <div class="head-btn">
            <a
              id="edit-button"
              class="btn"
              @click="jump(1)">
              <simple-line-icons
                icon="pencil"
                color="white"
                class="icon"
                size="small"/>
              修改课程
            </a>
            <a
              v-b-modal.delete
              id="delete-button"
              class="btn">
              <simple-line-icons
                icon="trash"
                color="white"
                class="icon"
                size="small"/>
              删除课程</a>
          </div>
          <ConfirmModal
            id="delete"
            title="确认删除"
            text="您确定要删除该课程吗？"
            @click="delete_message"/>
        </div>
      </div>
      <div class="table-div">
        <table
          class="table"
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
            <tr>
              <td class="head-td">
                课程简介
              </td>
              <td
                id="my-intro"
                class="content-td">
                {{ course.description }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Basic>
</template>

<script>
import Alert from '../../components/alert'
import Basic from '../basic/basic'
import ConfirmModal from '../components/confirm_modal'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'BackendCourseDetail',
  components: { Alert, ConfirmModal, Basic },
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '课程管理',
          href: '/admin/course'
        },
        {
          text: this.$route.query.course_id.toString(),
          active: true
        }
      ],
      test_router: -1,
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      course: {
        codename: '',
        name: '',
        time: '',
        price: '',
        reward_percent: '',
        created_at: '',
        updated_at: '',
        description: ''
      }
    }
  },
  created: function () {
    axios
      .get(
        'http://localhost/api/v1/courses/backstage/course-management/get-course-detail',
        {
          params: {
            course_id: this.$route.query.course_id
          }
        }
      )
      .then(response => {
        this.course.codename = response.data.codename
        this.course.title = response.data.title
        this.course.expire_duration = response.data.expire_duration
          .replace('P', '')
          .replace('DT', '天')
          .replace('H', '小时')
          .replace('M', '分钟')
          .replace('S', '秒钟')
        this.course.price = response.data.price
        this.course.reward_percent = response.data.reward_percent
        this.course.created_at = response.data.created_at
          .replace('T', ' ')
          .substring(0, 19)
        this.course.updated_at = response.data.updated_at
          .replace('T', ' ')
          .substring(0, 19)
        this.course.description = response.data.description
      })
      .catch(error => {
        this.wrong_count_down = 0
        this.success_count_down = 0
        this.error_message = this.init_error_message(error.response.data.message)
        this.wrong_count_down = 5
      })
  },
  methods: {
    jump: function (id) {
      this.test_router = id
      this.$router.push({
        name: 'EditCourse',
        query: { course_id: this.$route.query.course_id }
      })
    },
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        default:
          return '数据库查询出错'
      }
    },
    delete_message: function () {
      axios
        .post(
          'http://localhost/api/v1/courses/backstage/course-management/delete-course/',
          qs.stringify({
            course_id: this.$route.query.course_id
          })
        )
        .then(response => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = '删除课程成功'
          this.success_count_down = 3
          setTimeout(this.$router.push({ name: 'CourseManagement' }), 3000)
        })
        .catch(error => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = this.init_error_message(error.response.data.message)
          this.wrong_count_down = 5
        })
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px 0 15px;
  margin: 25px 0;
  color: #204269;
}

#my-intro {
  text-align: left;
}

.table-div {
  padding-right: 15px;
  padding-left: 15px;
  overflow-x: auto;
}

.my-in-btn {
  margin-right: auto;
  margin-left: 50px;
}

.head-td {
  width: 220px;
  max-width: 220px;
  font-weight: bold;
  color: #337ab7;
  background-color: #f3f4f6;
}

.content-td {
  color: #748085;
}

table {
  margin-bottom: 20px;
  font-size: 1rem;
  border-top: 1px solid #d3d9df;
  border-bottom: 1px solid #d3d9df;
}

h1 {
  text-align: left;
}

td {
  word-break: break-all;
  vertical-align: middle;
}

.btn {
  margin-left: 3px;
  border: 1px solid #d3d9df;
}

#edit-button {
  color: white;
  background-color: #4db14d;
}

#edit-button:hover,
#edit-button:active {
  background-color: #449c44;
}

#delete-button {
  color: white;
  background-color: #dd514c;
}

#delete-button:hover,
#delete-button:active {
  background-color: #ba2d28;
}
</style>
