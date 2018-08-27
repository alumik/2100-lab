<template>
  <div id="message-board">
    <div>
      <b-modal
        id="reply-popup"
        hide-footer
        title="回复留言">
        <textarea
          id="reply-input"
          v-model="new_reply"
          class="textarea-style"
          placeholder="请输入回复"
          @keyup.enter="reply_comment"/>
        <div>
          <b-btn @click="hide_reply_popup">
            取消
          </b-btn>
          <b-btn
            variant="primary"
            @click="reply_comment(reply_comment_id)">
            回复
          </b-btn>
        </div>
      </b-modal>
    </div>
    <div>
      <b-modal
        id="reply-list-popup"
        hide-footer
        title="全部回复">
        <div
          v-for="i in replies.length"
          id="replies-list"
          :key="i">
          <br>
          <div>
            <b-row>
              <b-col
                class="text-align-left"
                cols="4">
                {{ replies[i-1].username }}
              </b-col>
              <b-col cols="6">
                <label class="time-style">&emsp;
                  {{ replies[i-1].created_at }}回复
                </label>
              </b-col>
              <b-col
                v-if="replies[i-1].username === $store.state.user.username"
                class="delete-comment"
                @click="delete_list_comment(i-1,replies[i-1].comment_id)">
                <label>×</label>
              </b-col>
            </b-row>
            <b-row class="text-align-left">
              <p class="message-content">{{ replies[i-1].content }}</p>
            </b-row>
          </div>
          <b-row class="text-align-right">
            <b-col>
              {{ replies[i-1].up_votes }}
              <b-img
                :src="replies[i-1].up_voted === true ? up_icon_after : up_icon_before"
                class="vote-style "
                @click="modal_up_vote_reply(i-1, replies[i-1].comment_id)"/>
              &emsp; &emsp;{{ replies[i-1].down_votes }}
              <b-img
                :src="replies[i-1].down_voted === true ? down_icon_after : down_icon_before"
                class="vote-style "
                @click="modal_down_vote_reply(i-1, replies[i-1].comment_id)"/>
            </b-col>
          </b-row>
        </div>
        <div>
          <Pagination
            id="popup-pagination"
            :rows="modal_rows"
            :perpage="modal_page_limit"
            @change="change_list_page"/>
        </div>
        <div>
          <b-btn @click="hide_reply_list_popup">
            返回
          </b-btn>
        </div>
      </b-modal>
    </div>
    <div v-if="!can_comment">该课程已禁止评论！</div>
    <div v-if="can_comment">
      <b-alert
        :show="created_test"
        variant="danger"
        dismissible
        fade
        @dismissed="created_test=false">
        {{ created_error_msg }}
      </b-alert>
      <b-alert
        :show="getallmessage_test"
        variant="danger"
        dismissible
        fade
        @dismissed="getallmessage_test=false">
        {{ getallmessage_error_msg }}
      </b-alert>
      <b-alert
        :show="up_vote_test"
        variant="danger"
        dismissible
        fade
        @dismissed="up_vote_test=false">
        {{ up_vote_error_msg }}
      </b-alert>
      <b-alert
        :show="down_vote_test"
        variant="danger"
        dismissible
        fade
        @dismissed="down_vote_test=false">
        {{ down_vote_error_msg }}
      </b-alert>
      <b-alert
        :show="delete_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="delete_message_test=false">
        {{ delete_message_error_msg }}
      </b-alert>
      <b-alert
        :show="add_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="add_message_test=false">
        {{ add_message_error_msg }}
      </b-alert>
      <div class="form-style">
        <div
          v-for="index in message_list.length"
          id="comment"
          :key="index"
          class="piece-of-message">
          <div id="piece-of-message">
            <b-row>
              <b-col cols="1">
                <img
                  id="userimg"
                  class="userimg"
                  src="../../assets/logo.png">
              </b-col>
              <b-col cols="2">
                {{ message_list[index-1].username }}
              </b-col>
              <b-col cols="4">
                <label class="time-style">&emsp;{{ message_list[index-1].created_at }}评论</label>
              </b-col>
              <b-col>
                <label
                  id="reply-button"
                  @click="want_reply(message_list[index-1].comment_id)">
                  回复
                </label>
                <label
                  id="watch-more"
                  @click="watch_all_replies(message_list[index-1].comment_id)">
                  更多回复
                </label>
              </b-col>
              <b-col
                v-if="message_list[index-1].username === $store.state.user.username"
                id="delete-button"
                class="delete-comment"
                @click="delete_comment(message_list[index-1].comment_id)">
                <label>×</label>
              </b-col>
            </b-row>
            <p class="message-content">{{ message_list[index-1].content }}</p>
          </div>
          <b-row class="text-align-right">
            <b-col>
              {{ message_list[index-1].up_votes }}
              <b-img
                id="praise-button"
                :src="message_list[index-1].up_voted === true ? up_icon_after : up_icon_before"
                class="vote-style "
                @click="up_vote(index-1,message_list[index-1].comment_id)"/>
              &emsp; &emsp;{{ message_list[index-1].down_votes }}
              <b-img
                id="detest-button"
                :src="message_list[index-1].down_voted === true ? down_icon_after : down_icon_before"
                class="vote-style "
                @click="down_vote(index-1,message_list[index-1].comment_id)"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div
                v-for="i in message_list[index-1].replies.length"
                :key="i">
                <div>
                  <b-row>
                    <b-col class="text-align-left">
                      {{ message_list[index-1].replies[i-1].username }}
                      <label class="time-style">&emsp;
                        {{ message_list[index-1].replies[i-1].created_at }}
                        回复{{ message_list[index-1].username }}</label>
                    </b-col>
                    <b-col
                      v-if="message_list[index-1].replies[i-1].username === $store.state.user.username"
                      class="delete-comment"
                      @click="delete_comment(message_list[index-1].replies[i-1].comment_id)">
                      <label>×</label>
                    </b-col>
                  </b-row>
                  <p class="message-content">{{ message_list[index-1].replies[i-1].content }}</p>
                </div>
                <b-row class="text-align-right">
                  <b-col>
                    {{ message_list[index-1].replies[i-1].up_votes }}
                    <b-img
                      :src="message_list[index-1].replies[i-1].up_voted === true ? up_icon_after : up_icon_before"
                      class="vote-style "
                      @click="up_vote_child_reply(index-1, i-1, message_list[index-1].replies[i-1].comment_id)"/>
                    &emsp; &emsp;{{ message_list[index-1].replies[i-1].down_votes }}
                    <b-img
                      :src="message_list[index-1].replies[i-1].down_voted === true ? down_icon_after : down_icon_before"
                      class="vote-style "
                      @click="down_vote_child_reply(index-1, i-1, message_list[index-1].replies[i-1].comment_id)"/>
                  </b-col>
                </b-row>
              </div>
            </b-col>
          </b-row>
        </div>
      </div>
      <div>
        <textarea
          id="input-message"
          v-model="new_msg"
          class="textarea-style"
          placeholder="请输入评论"
          @keyup.enter="add_comment"/>
        <br>
        <div
          id="commit-button"
          class="commit-button-style">
          <b-button
            @click="add_comment">评论</b-button>
        </div>
      </div>
      <div>
        <Pagination
          id="pagination"
          :rows="rows"
          :perpage="page_limit"
          @change="change_page"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import Pagination from '../../components/pagination'

export default {
  name: 'MessageBoard',
  components: {
    Pagination
  },
  props: {
    course_id: {
      type: Number,
      default: 0
    }
  },
  data () {
    return {
      username: '小可爱',
      new_msg: '',
      message_list: [],
      created_test: false,
      created_error_msg: '',
      getallmessage_test: false,
      getallmessage_error_msg: '',
      up_vote_test: false,
      up_vote_error_msg: '',
      down_vote_test: false,
      down_vote_error_msg: '',
      add_message_test: false,
      add_message_error_msg: '',
      delete_message_test: false,
      delete_message_error_msg: '',
      page_limit: 1,
      page: 1,
      rows: 0,
      modal_page_limit: 2,
      modal_page: 1,
      modal_rows: 0,
      up_icon_before: require('../../assets/up-before.png'),
      up_icon_after: require('../../assets/up-after.png'),
      down_icon_before: require('../../assets/down-before.png'),
      down_icon_after: require('../../assets/down-after.png'),
      can_comment: true,
      reply_comment_id: 0,
      new_reply: '',
      child_reply_num: 0,
      get_all_reply_id: 0,
      replies: []
    }
  },
  created: function () {
    this.page = this.$route.query.page
    this.getallmessage()
  },
  methods: {
    change_list_page: function (page) {
      let that = this
      that.modal_page = page
      that.get_replies(that.get_all_reply_id)
    },
    hide_reply_list_popup: function () {
      this.$root.$emit('bv::hide::modal', 'reply-list-popup')
    },
    hide_reply_popup: function () {
      this.$root.$emit('bv::hide::modal', 'reply-popup')
    },
    want_reply: function (commentId) {
      this.reply_comment_id = commentId
      this.$root.$emit('bv::show::modal', 'reply-popup')
    },
    getallmessage: function () {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/get-course-comments/',
          {
            params: {
              course_id: that.course_id,
              page_limit: that.page_limit,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.rows = response.data.count
          that.message_list = response.data.content
          that.can_comment = true
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.getallmessage_test = true
            that.getallmessage_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.getallmessage_test = true
            that.getallmessage_error_msg = that.$t('error.access_denied')
          }
        })
    },
    up_vote: function (index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/up-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.message_list[index].up_votes = response.data.up_votes
            that.message_list[index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.message_list[index].up_votes = response.data.up_votes
            that.message_list[index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    up_vote_child_reply: function (index, replyIndex, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/up-vote-comment?' +
          'comment_id=' +
          msgCommentId
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.message_list[index].replies[replyIndex].up_votes = response.data.up_votes
            that.message_list[index].replies[replyIndex].up_voted = true
          } else if (response.data.up_voted === false) {
            that.message_list[index].replies[replyIndex].up_votes = response.data.up_votes
            that.message_list[index].replies[replyIndex].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    modal_up_vote_reply: function (replyIndex, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/up-vote-comment?' +
          'comment_id=' +
          msgCommentId
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.replies[replyIndex].up_votes = response.data.up_votes
            that.replies[replyIndex].up_voted = true
          } else if (response.data.up_voted === false) {
            that.replies[replyIndex].up_votes = response.data.up_votes
            that.replies[replyIndex].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    down_vote: function (index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/down-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].down_votes = response.data.down_votes
            that.message_list[index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.message_list[index].down_votes = response.data.down_votes
            that.message_list[index].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    down_vote_child_reply: function (index, replyIndex, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/down-vote-comment?' +
          'comment_id=' +
          msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].replies[replyIndex].down_votes = response.data.down_votes
            that.message_list[index].replies[replyIndex].down_voted = true
          } else if (response.data.down_voted === false) {
            that.message_list[index].replies[replyIndex].down_votes = response.data.down_votes
            that.message_list[index].replies[replyIndex].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    modal_down_vote_reply: function (replyIndex, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/down-vote-comment?' +
          'comment_id=' +
          msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.replies[replyIndex].down_votes = response.data.down_votes
            that.replies[replyIndex].down_voted = true
          } else if (response.data.down_voted === false) {
            that.replies[replyIndex].down_votes = response.data.down_votes
            that.replies[replyIndex].down_voted = false
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.down_vote_test = true
            that.down_vote_error_msg = that.$t('error.access_denied')
          }
        })
    },
    watch_all_replies: function (commentId) {
      this.get_all_reply_id = commentId
      this.get_replies(commentId)
      this.$root.$emit('bv::show::modal', 'reply-list-popup')
    },
    get_replies: function (commentId) {
      let that = this
      axios
        .get(
          'http://localhost:8000/api/v1/courses/forestage/play/get-replies/', {
            params: {
              comment_id: commentId,
              page_limit: that.modal_page_limit,
              page: that.modal_page
            }
          })
        .then(function (response) {
          that.replies = response.data.content
          that.modal_rows = response.data.count
        })
    },
    delete_comment: function (commentId) {
      let that = this
      axios
        .post(
          'http://localhost:8000/api/v1/courses/forestage/play/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            alert(that.$t('prompt.object_deleted'))
            that.getallmessage()
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.access_denied')
          }
        })
    },
    delete_list_comment: function (index, commentId) {
      let that = this
      axios
        .post(
          'http://localhost:8000/api/v1/courses/forestage/play/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            alert(that.$t('prompt.object_deleted'))
            that.replies.splice(index, 1)
            that.get_replies(that.get_all_reply_id)
            that.getallmessage()
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.delete_message_test = true
            that.delete_message_error_msg = that.$t('error.access_denied')
          }
        })
    },
    add_comment: function () {
      let that = this
      const value = that.new_msg && that.new_msg.trim()
      if (!value) {
        return
      }
      axios
        .post(
          'http://localhost:8000/api/v1/courses/forestage/play/add-comment/',
          qs.stringify({
            content: value,
            course_id: that.course_id
          })
        )
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.getallmessage()
          }
        })
        .catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.add_message_test = true
            that.add_message_error_msg = that.$t('error.object_not_found')
          } else if (error.response.data.message === 'Access denied.') {
            that.add_message_test = true
            that.add_message_error_msg = that.$t('error.access_denied')
          } else if (
            error.response.data.message === 'Commenting is not allowed.'
          ) {
            that.add_message_test = true
            that.add_message_error_msg = that.$t(
              'prompt.user_comment_not_allowed'
            )
          }
        })
      that.new_msg = ''
    },
    reply_comment: function () {
      let that = this
      const value = that.new_reply && that.new_reply.trim()
      if (!value) {
        return
      }
      if (that.reply_comment_id !== 0) {
        axios
          .post(
            'http://localhost:8000/api/v1/courses/forestage/play/add-comment/',
            qs.stringify({
              content: value,
              course_id: that.course_id,
              reply_to_id: that.reply_comment_id
            })
          )
          .then(function (response) {
            if (response.data.message === 'Success.') {
              that.getallmessage()
            }
          })
          .catch(function (error) {
            if (error.response.data.message === 'Object not found.') {
              that.add_message_test = true
              that.add_message_error_msg = that.$t('error.object_not_found')
            } else if (error.response.data.message === 'Access denied.') {
              that.add_message_test = true
              that.add_message_error_msg = that.$t('error.access_denied')
            } else if (
              error.response.data.message === 'Commenting is not allowed.'
            ) {
              that.add_message_test = true
              that.add_message_error_msg = that.$t(
                'prompt.user_comment_not_allowed'
              )
            }
          })
      }
      that.$root.$emit('bv::hide::modal', 'reply-popup')
      that.new_reply = ''
    },
    change_page: function (page) {
      this.page = page
      this.getallmessage()
    }
  }
}
</script>

<style scoped>
.time-style {
  color: #adb5bd;
}

.textarea-style {
  width: 100%;
  height: 30%;
  padding: 0;
  resize: none;
  border: solid 2px #ddd;
}

.text-align-right {
  text-align: right;
}

.textarea-style:focus {
  border: solid 2px #cce5ff;
}

.commit-button-style {
  width: 100%;
  text-align: right;
}

.form-style {
  width: 100%;
  padding: 0;
  text-align: right;
}

.message-content {
  margin-bottom: 5px;
}

.piece-of-message {
  width: 98%;
  height: 50%;
  margin: 10px;
  text-align: left;
}

#operator {
  text-align: left;
}

.vote-style {
  height: 25px;
}

.vote-style:hover {
  filter: brightness(110%);
}

.userimg {
  width: 40px;
  height: 40px;
  margin-right: 20px;
  border-radius: 50%;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.text-align-left {
  text-align: left;
}

.delete-comment {
  color: #f00;
  text-align: right;
}
</style>
