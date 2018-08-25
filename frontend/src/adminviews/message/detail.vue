<template>
  <Basic
    :items="items"
    class="my-basic">
    <div class="body">
      <div class="title">
        <h1>留言详情</h1>
        <div class="buttons">
          <a
            v-b-modal.reply
            id="reply-button"
            class="btn btn-lg"
            @click="reply_id=message.comment_id">
            <simple-line-icons
              icon="pencil"
              color="white"
              class="icon"
              size="small"/>
            回复
          </a>
          <InputModal
            id="reply"
            title="回复留言"
            placeholder="请输入你要回复的内容"
            @click="reply_message"/>
          <a
            v-b-modal.delete
            id="delete-button"
            class="btn btn-lg">
            <simple-line-icons
              icon="trash"
              color="white"
              class="icon"
              size="small"/>
            删除</a>
          <ConfirmModal
            id="delete"
            title="确认删除"
            text="您确定要删除此条留言吗？"
            @click="delete_message"/>
        </div>
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
import Alert from '../../components/alert'
export default {
  name: 'MessageDetail',
  components: { Alert, DetailTable, Basic, InputModal, ConfirmModal },
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
      axios.post('http://localhost:8000/api/v1/courses/backstage/comment-management/delete-comment/',
        qs.stringify({
          comment_id: that.$route.query.message_id
        }))
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.wrong = '你所删除的留言不存在，删除失败！'
            that.wrong_count_down = that.dismiss_second
            that.success = '您已经成功删除此留言。'
            that.success_count_down = that.dismiss_second
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
      axios.post('http://localhost:8000/api/v1/courses/backstage/comment-management/add-comment/',
        qs.stringify({
          reply_to_id: that.$route.query.message_id,
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
  .body {
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
    padding: 0 15px 10px 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    color: #23527c;
    border-bottom: 1px solid #eef1f5;
  }

  h1 {
    text-align: left;
  }

  td {
    vertical-align: middle;
  }

  .buttons {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    text-align: right;
  }

  .btn {
    margin-right: 3px;
    margin-left: 3px;
    border: 1px solid #d3d9df;
  }

  #reply-button {
    color: white;
    background-color: #4db14d;
  }

  #reply-button:hover,
  #reply-button:active {
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
