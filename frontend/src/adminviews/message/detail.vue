<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <div class="title">
        <h1>留言详情</h1>
        <div class="buttons">
          <button
            v-b-modal.reply
            type="button"
            class="btn btn-lg">
            回复留言
          </button>
          <InputModal
            id="reply"
            title="回复留言"
            placeholder="请输入你要回复的内容"
            @click="reply_message"/>
          <button
            v-b-modal.delete
            type="button"
            class="btn btn-lg">
            删除留言
          </button>
          <ConfirmModal
            id="delete"
            title="确认删除"
            text="您确定要删除此条留言吗？"
            @click="delete_message"/>
        </div>
      </div>
      <b-alert
        :show="wrong_count_down"
        class="my-alert"
        variant="danger"
        dismissible
        @dismissed="wrong_count_down=0"
        @dismiss_count_down="count_down_changed(wrong_count_down)">
        {{ wrong }}
      </b-alert>
      <b-alert
        :show="success_count_down"
        class="my-alert"
        variant="success"
        dismissible
        @dismissed="success_count_down=0"
        @dismiss_count_down="count_down_changed(success_count_down)">
        {{ success }}
      </b-alert>
      <DetailTable
        :titles="titles"
        :data="message"/>
    </div>
  </Basic>
</template>

<script>
import ConfirmModal from '../components/ConfirmModal'
import InputModal from '../components/InputModal'
import Basic from '../basic/basic'
import DetailTable from '../components/detail_table'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'MessageDetail',
  components: { DetailTable, Basic, InputModal, ConfirmModal },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '留言管理',
        href: '/admin/message'
      }, {
        text: this.$route.query.message_id,
        active: true
      }],
      titles: ['留言日期', '用户', '课程代码', '课程名', '点赞数', '点踩数', '状态', '删除日期', '内容'],
      message: [],
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: '',
      success_count_down: 0,
      success: ''
    }
  },
  created () {
    const that = this
    axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-detail/',
      {params: {
        comment_id: that.$route.query.message_id
      }})
      .then(function (response) {
        that.message = that.computed_message(response.data)
      })
      .catch(function (error) {
        that.wrong = '获取留言详情失败！' + error
        that.wrong_count_down = that.dismiss_second
      })
  },
  methods: {
    search: function () {
      const that = this
      axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/get-comment-detail/',
        {params: {
          comment_id: that.$route.query.message_id
        }})
        .then(function (response) {
          that.message = that.computed_message(response.data)
        })
        .catch(function (error) {
          that.wrong = '获取留言详情失败！' + error
          that.wrong_count_down = that.dismiss_second
        })
    },
    compute_state: function (deleted) {
      if (deleted) {
        return '已删除'
      } else {
        return '未删除'
      }
    },
    count_down_changed: function (val) {
      const that = this
      let t = setInterval(function () {
        val -= 1
        if (that.val === 0) {
          clearInterval(t)
        }
      }, 1000)
    },
    computed_message: function (val) {
      let temp = new Array(9)
      temp[0] = (val.created_at + '').slice(0, 10)
      temp[1] = val.username
      temp[2] = val.course_codename
      temp[3] = val.course_title
      temp[4] = val.up_votes
      temp[5] = val.down_votes
      if (val.is_deleted) {
        temp[6] = '已删除'
      } else {
        temp[6] = '未删除'
      }
      if (val.deleted_at === null) {
        temp[7] = ''
      } else {
        temp[7] = (val.deleted_at + '').slice(0, 10)
      }
      temp[8] = val.content
      return temp
    },
    delete_message: function () {
      const that = this
      axios.get('http://localhost:8000/api/v1/courses/backstage/comment-management/delete-comment/',
        {params: {
          comment_id: that.$route.query.message_id
        }})
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
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
          course_codename: that.message[2],
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
    }
  }
}
</script>

<style scoped>
  .my-basic {
    min-width: 1000px;
  }

  .title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
  }

  h1 {
    padding-left: 15px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    text-align: right;
  }

  td {
    vertical-align: middle;
  }

  .btn {
    margin-right: 10px;
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

  .my-alert {
    padding-right: 15px;
    padding-left: 15px;
  }
</style>
