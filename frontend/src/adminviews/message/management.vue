<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>留言列表</h1>
      <div class="table-div">
        <b-alert
          :show="wrong_count_down"
          variant="danger"
          dismissible
          @dismissed="wrong_count_down=0"
          @dismiss_count_down="count_down_changed(wrong_count_down)">
          {{ wrong }}
        </b-alert>
        <b-alert
          :show="success_count_down"
          variant="success"
          dismissible
          @dismissed="success_count_down=0"
          @dismiss_count_down="count_down_changed(success_count_down)">
          {{ success }}
        </b-alert>
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
            <tr align="center">
              <td/>
              <td class="xs-td">
                <div class="input-group-sm">
                  <input
                    v-model="user"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="xs-td">
                <div class="input-group-sm">
                  <input
                    v-model="course_code"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="xs-td">
                <div class="input-group-sm">
                  <input
                    v-model="course_name"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="search">
                </div>
              </td>
              <td class="lg-td"/>
              <td class="s-td">
                <div>
                  <select
                    v-model="state"
                    class="selectpicker"
                    @change="search">
                    <option value="whole">全部</option>
                    <option value="reserved">未删除</option>
                    <option value="deleted">已删除</option>
                  </select>
                </div>
              </td>
              <td class="md-td"/>
            </tr>
            <tr
              v-for="message in messages"
              :key="message.id">
              <td>{{ compute_date(message.created_at) }}</td>
              <td>{{ message.username }}</td>
              <td>{{ message.course_codename }}</td>
              <td>{{ message.course_title }}</td>
              <td>{{ message.content }}</td>
              <td> {{ compute_state(message.is_deleted) }} </td>
              <td class="buttons">
                <button
                  type="button"
                  class="btn btn-xs"
                  @click="to_detail(message.comment_id + '')">
                  详情
                </button>
                <button
                  v-b-modal.reply
                  type="button"
                  class="btn"
                  @click="reply_id=message.course_codename">
                  回复
                </button>
                <button
                  v-b-modal.delete
                  type="button"
                  class="btn"
                  @click="delete_id=message.comment_id">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <InputModal
        id="reply"
        :input="reply"
        title="回复留言"
        placeholder="请输入你要回复的内容"
        @click="reply_message"/>
      <ConfirmModal
        id="delete"
        title="确认删除"
        text="您确定要删除此条留言吗？"
        @click="delete_message"/>
      <Pagination
        :rows="rows"
        :perpage="per_page"
        @change="change_page"/>
    </div>
  </Basic>
</template>

<script>
import Pagination from '../../components/pagination'
import ConfirmModal from '../components/ConfirmModal'
import InputModal from '../components/InputModal'
import Basic from '../basic/basic'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'MessageManagement',
  components: { Basic, InputModal, ConfirmModal, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '留言管理',
        active: true
      }],
      rows: 0,
      messages: null,
      titles: [
        { label: '日期' },
        { label: '用户' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '留言' },
        { label: '状态' },
        { label: '操作' }
      ],
      user: '',
      course_code: '',
      course_name: '',
      state: '',
      reply: '',
      page_jump: false,
      per_page: 2,
      page: 1,
      wrong: '',
      success: '',
      dismiss_second: 5,
      wrong_count_down: 0,
      success_count_down: 0,
      delete_id: '',
      reply_id: ''
    }
  },
  created () {
    const that = this
    axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-list/', { params: {
      page_limit: that.per_page,
      page: that.page
    }})
      .then(function (response) {
        that.messages = response.data.content
        that.rows = response.data.count
      })
      .catch(function (error) {
        that.wrong = '加载留言失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'MessageDetail', query: {message_id: val} })
    },
    compute_date: function (date) {
      return date.slice(0, 10)
    },
    compute_state: function (deleted) {
      if (deleted) {
        return '已删除'
      } else {
        return '未删除'
      }
    },
    search: function () {
      const that = this
      let state
      if (that.state === 'whole' || that.state === '') {
        state = '0'
      } else if (that.state === 'reserved') {
        state = '1'
      } else {
        state = '2'
      }
      axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-list/',
        {params: {
          username: that.user,
          course_codename: that.course_code,
          course_title: that.course_name,
          is_deleted: state,
          page_limit: that.per_page,
          page: that.page
        }})
        .then(function (response) {
          that.messages = response.data.content
          that.rows = response.data.count
        })
        .catch(function (error) {
          that.wrong = '查询留言失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    change_page: function (page) {
      this.page = page
      this.search()
    },
    delete_message: function () {
      const that = this
      axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/delete-comment/',
        {params: {
          comment_id: that.delete_id
        }})
        .then(function (response) {
          if (response.data.message === 'Comment deleted.') {
            that.success = '您已经成功删除此留言。'
            that.success_count_down = that.dismiss_second
          } else {
            that.wrong = '你所删除的留言不存在，删除失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '删除失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
      this.search()
    },
    reply_message: function (val) {
      const that = this
      axios.post('http://localhost:8000/api/v1/courses/backstage/comment-management/add-comment/',
        qs.stringify({
          course_codename: that.reply_id,
          comment_content: val
        }))
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.success = '您已经成功回复此留言。'
            that.success_count_down = that.dismiss_second
          } else {
            that.wrong = '您所回复留言的课程不存在，回复失败！'
            that.wrong_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '回复失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
      this.search()
    },
    count_down_changed: function (val) {
      const that = this
      let t = setInterval(function () {
        val -= 1
        if (that.val === 0) {
          clearInterval(t)
        }
      }, 1000)
    }
  }
}
</script>

<style scoped>
  .my-basic {
    min-width: 1300px;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .buttons {
    display: flex;
    padding-left: 30px;
  }

  table {
    font-size: 1.2em;
    border: 1px solid #d3d9df;
  }

  td {
    vertical-align: middle;
  }

  td button {
    margin-right: 7px;
    margin-left: 7px;
    border-radius: 10px;
    outline: none;
    box-shadow: #adb5bd inset;
  }

  select {
    width: 130px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }

  .table-div {
    padding-right: 15px;
    padding-left: 15px;
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

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .xs-td {
    width: 160px;
  }

  .s-td {
    width: 200px;
  }

  .md-td {
    width: 270px;
  }

  .lg-td {
    width: 350px;
  }
</style>
