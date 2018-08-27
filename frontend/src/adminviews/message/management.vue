<template>
  <Basic :items="items">
    <div class="body">
      <div class="head-container">
        <div class="head-title">
          <h1>{{ $t("message.title") }}</h1>
        </div>
        <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      </div>
      <Alert
        :count_down="wrong_count_down"
        :instruction="wrong"
        variant="danger"
        @decrease="wrong_count_down-1"
        @zero="wrong_count_down=0"/>
      <Alert
        :count_down="success_count_down"
        :instruction="success"
        variant="success"
        @decrease="success_count_down-1"
        @zero="success_count_down=0"/>
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
            <tr align="center">
              <td class="s-td"/>
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
                    <option value="whole">{{ $t('message.state1') }}</option>
                    <option value="reserved">{{ $t('message.state2') }}</option>
                    <option value="deleted">{{ $t('message.state3') }}</option>
                  </select>
                </div>
              </td>
              <td class="md-td"/>
            </tr>
            <tr
              v-for="message in messages"
              :key="message.id">
              <td id="date">{{ compute_date(message.created_at) }}</td>
              <td>{{ compute_username(message.username) }}</td>
              <td>{{ message.course_codename }}</td>
              <td>{{ message.course_title }}</td>
              <td>{{ compute_message(message.content) }}</td>
              <td id="state"> {{ compute_state(message.is_deleted) }} </td>
              <td class="buttons">
                <a
                  id="detail-button"
                  class="btn"
                  @click="to_detail(message.comment_id + '')">
                  <simple-line-icons
                    icon="bubble"
                    color="#5b9bd1"
                    class="icon"
                    size="small"/>
                  {{ $t('message.detail') }}
                </a>
                <a
                  v-b-modal.reply
                  id="reply-button"
                  class="btn"
                  @click="reply_id=message.comment_id">
                  <simple-line-icons
                    icon="pencil"
                    color="green"
                    class="icon"
                    size="small"/>
                  {{ $t('message.reply') }}
                </a>
                <a
                  v-b-modal.delete
                  id="delete-button"
                  class="btn"
                  @click="delete_id=message.comment_id">
                  <simple-line-icons
                    icon="trash"
                    color="#e60000"
                    class="icon"
                    size="small"/>
                  {{ $t('message.delete') }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
        <Pagination
          :rows="rows"
          :perpage="per_page"
          @change="change_page"/>
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
import Alert from '../../components/alert'
export default {
  name: 'MessageManagement',
  components: { Alert, Basic, InputModal, ConfirmModal, Pagination },
  data () {
    return {
      items: [
        {
          text: this.$t('message.breadcrumb1'),
          href: '/admin/main'
        },
        {
          text: this.$t('message.breadcrumb2'),
          active: true
        }
      ],
      rows: 0,
      messages: null,
      titles: [
        { label: this.$t('message.header1') },
        { label: this.$t('message.header2') },
        { label: this.$t('message.header3') },
        { label: this.$t('message.header4') },
        { label: this.$t('message.header5') },
        { label: this.$t('message.header6') },
        { label: this.$t('message.header7') }
      ],
      user: '',
      course_code: '',
      course_name: '',
      state: '',
      reply: '',
      page_jump: false,
      per_page: 20,
      page: 1,
      wrong: '',
      success: '',
      dismiss_second: 5,
      wrong_count_down: 0,
      success_count_down: 0,
      delete_id: '',
      reply_id: '',
      num_pages: 0
    }
  },
  created () {
    const that = this
    axios
      .get(
        'http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-list/',
        {
          params: {
            page_limit: that.per_page,
            page: that.page
          }
        }
      )
      .then(function (response) {
        that.messages = response.data.content
        that.rows = response.data.count
        if (response.data.num_pages === 0) {
          that.num_pages = 1
        } else {
          that.num_pages = response.data.num_pages
        }
      })
      .catch(function (error) {
        that.wrong = '加载留言失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    to_detail: function (val) {
      this.page_jump = true
      this.$router.push({ name: 'MessageDetail', query: { message_id: val } })
    },
    compute_date: function (date) {
      return date.slice(0, 10)
    },
    compute_state: function (deleted) {
      if (deleted) {
        return this.$t('message.state3')
      } else {
        return this.$t('message.state2')
      }
    },
    compute_username: function (name) {
      let index = name.search('_deleted_')
      if (index !== -1) {
        return name.slice(0, index) + '（已删除）'
      } else {
        return name
      }
    },
    compute_message: function (content) {
      if (content.length > 7) {
        return content.slice(0, 7) + '...'
      } else {
        return content
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
      axios
        .get(
          'http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-list/',
          {
            params: {
              username: that.user,
              course_codename: that.course_code,
              course_title: that.course_name,
              is_deleted: state,
              page_limit: that.per_page,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.messages = response.data.content
          that.rows = response.data.count
          if (response.data.num_pages === 0) {
            that.num_pages = 1
          } else {
            that.num_pages = response.data.num_pages
          }
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
      axios
        .post(
          'http://localhost:8000/api/v1/courses/backstage/comment-management/delete-comment/',
          qs.stringify({
            comment_id: that.delete_id
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '你所删除的留言不存在，删除失败！'
            that.wrong_count_down = that.dismiss_second
          } else {
            that.search()
            that.success = '您已经成功删除此留言。'
            that.success_count_down = that.dismiss_second
          }
        })
        .catch(function (error) {
          that.wrong = '删除失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    reply_message: function (val) {
      const that = this
      axios
        .post(
          'http://localhost:8000/api/v1/courses/backstage/comment-management/add-comment/',
          qs.stringify({
            reply_to_id: that.reply_id,
            comment_content: val
          })
        )
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.search()
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

.buttons {
  padding: 10px;
  white-space: nowrap;
}

.table-div {
  padding-right: 15px;
  padding-left: 15px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  border-top: 1px solid #d3d9df;
}

td {
  font-size: 1rem;
  vertical-align: middle;
}

.btn {
  margin-right: 2px;
  margin-left: 2px;
  border: 1px solid #d3d9df;
}

#detail-button {
  color: #5b9bd1;
}

#reply-button {
  color: green;
}

#delete-button {
  color: #e60000;
}

#detail-button:hover {
  background-color: rgba(91, 155, 209, 0.2);
}

#reply-button:hover {
  background-color: rgba(0, 128, 0, 0.2);
}

#delete-button:hover {
  background-color: rgba(230, 0, 0, 0.2);
}

select {
  width: 130px;
  height: 30px;
  color: #2c3e50;
  border: 1px solid #ced4da;
  border-radius: 5px;
  outline: none;
}

option {
  font-size: 18px;
}

thead tr {
  font-weight: bold;
  color: #999;
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
