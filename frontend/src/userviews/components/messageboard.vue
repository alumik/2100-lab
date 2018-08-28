<template>
  <div id="message-board">
    <div class="text-align-left">
      {{ rows }}
      <simple-line-icons
        icon="bubble"
        size="small"
        color="#009966"/>
    </div>
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
          :key="i"
          class="reply-message">
          <div>
            <div>
              <div class="row1">
                <div class="row2">
                  <div class="row3">
                    {{ replies[i-1].username }}
                    <label
                      v-if="replies[i-1].user_is_vip === true"
                      class="vip-style">
                      V
                    </label>
                  </div>
                  <div class="comment-wrap">&emsp;
                    {{ replies[i-1].content }}
                  </div>
                </div>
                <div
                  v-if="replies[i-1].username ===
                  $store.state.user.username"
                  class="delete-comment"
                  @click="delete_list_comment(i-1,replies[i-1].comment_id)">
                  <label>删除</label>
                </div>
              </div>
              <div style="display: flex; flex-direction: row;">
                <label class="time-style">
                  {{ get_date(replies[i-1].created_at).substring(0,10) }}
                </label>
                <div>
                  &emsp;{{ replies[i-1].up_votes }}
                  <b-img
                    :src="replies[i-1].up_voted === true ? up_icon_after :
                    up_icon_before"
                    class="vote-style "
                    @click="modal_up_vote_reply
                  (i-1, replies[i-1].comment_id)"/>
                  &emsp; &emsp;{{ replies[i-1].down_votes }}
                  <b-img
                    :src="replies[i-1].down_voted === true ? down_icon_after
                    : down_icon_before"
                    class="vote-style "
                    @click="modal_down_vote_reply
                  (i-1, replies[i-1].comment_id)"/>
                </div>
              </div>
            </div>
          </div>
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
        :show="get_all_message_test"
        variant="danger"
        dismissible
        fade
        @dismissed="get_all_message_test=false">
        {{ get_all_message_error_msg }}
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
      <div
        class="comment-style" >
        <div class="user-avatar">
          <img
            :src="$store.state.address + this.$store.state.user.avatar"
            class="userimg">
        </div>
        <div class="message-area">
          <textarea
            id="input-message"
            v-model="new_msg"
            class="textarea-style"
            placeholder="请输入留言"
            @keyup.enter="add_comment"/>
          <div
            id="commit-button"
            class="commit-button-style">
            <b-button
              class="add_comment"
              @click="add_comment">发表<br>评论</b-button>
          </div>
        </div>
      </div>
      <div
        v-for="index in message_list.length"
        id="piece-of-message"
        :key="index"
        class="piece-of-message">
        <div class="user-avatar">
          <img
            :src="$store.state.address + message_list[index-1].avatar"
            class="userimg">
        </div>
        <div class="message-list-area">
          <div class="message-username">
            <div class="message-list-username">
              {{ message_list[index-1].username }}
              <label
                v-if="message_list[index-1].user_is_vip === true"
                class="vip-style">
                V
              </label>
            </div>
            <div
              v-if="message_list[index-1].username ===
              $store.state.user.username"
              id="delete-button"
              class="delete-comment"
              @click="delete_comment(message_list[index-1].comment_id)">
              删除</div>
          </div>
          <div class="comment-wrap">{{ message_list[index-1].content }}
          </div>
          <div class="time-remind">
            <div
              class="time-style">
              {{ get_date(message_list[index-1].created_at) }}
            </div>
            <div class="margin-right-1">
              {{ message_list[index-1].up_votes }}
              <b-img
                id="praise-button"
                :src="message_list[index-1].up_voted === true ?
                up_icon_after : up_icon_before"
                class="vote-style "
                @click="up_vote(index-1,message_list[index-1].comment_id)"/>
              &emsp; {{ message_list[index-1].down_votes }}
              <b-img
                id="detest-button"
                :src="message_list[index-1].down_voted === true ?
                down_icon_after : down_icon_before"
                class="vote-style "
                @click="down_vote
              (index-1,message_list[index-1].comment_id)"/>
            </div>
            <div
              id="reply-button"
              @click="want_reply(message_list[index-1].comment_id)">
              回复
            </div>
          </div>
          <div
            v-for="i in message_list[index-1].replies.length"
            :key="i"
            class="reply-message">
            <div>
              <div>
                <div class="row1">
                  <div class="row2">
                    <div class="row3">
                      {{ message_list[index-1].replies[i-1].username }}
                      <label
                        v-if="message_list[index-1].replies[i-1].user_is_vip
                        === true"
                        class="vip-style">
                        V
                      </label>
                    </div>
                    <div class="comment-wrap">&emsp;{{ message_list[index-1].
                    replies[i-1].content }}</div>
                  </div>
                  <div
                    v-if="message_list[index-1].replies[i-1].username ===
                    $store.state.user.username"
                    class="delete-comment"
                    @click="delete_comment(message_list[index-1].replies[i-1]
                    .comment_id)">
                    <label>删除</label>
                  </div>
                </div>
                <div style="display: flex; flex-direction: row;">
                  <label class="time-style">
                    {{ get_date(message_list[index-1].replies[i-1].created_at) }}
                  </label>
                  <div>
                    &emsp;{{ message_list[index-1].replies[i-1].up_votes }}
                    <b-img
                      :src="message_list[index-1].replies[i-1].up_voted ===
                      true ? up_icon_after : up_icon_before"
                      class="vote-style "
                      @click="up_vote_child_reply(index-1, i-1,
                                                  message_list[index-1].replies[i-1].comment_id)"/>
                    &emsp; &emsp;{{ message_list[index-1].replies[i-1].down_votes }}
                    <b-img
                      :src="message_list[index-1].replies[i-1].down_voted
                      === true ? down_icon_after : down_icon_before"
                      class="vote-style "
                      @click="down_vote_child_reply(index-1, i-1,
                                                    message_list[index-1].replies[i-1].comment_id)"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="message_list [index-1].reply_count !== 0"
            class="all-reply">
            <div class="margin-right-1">
              共{{ message_list [index-1].reply_count }}条回复
            </div>
            <div
              id="watch-more"
              class="look-all"
              @click="watch_all_replies(message_list[index-1].comment_id)">
              点击查看
            </div>
          </div>
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
      get_all_message_test: false,
      get_all_message_error_msg: '',
      up_vote_test: false,
      up_vote_error_msg: '',
      down_vote_test: false,
      down_vote_error_msg: '',
      add_message_test: false,
      add_message_error_msg: '',
      delete_message_test: false,
      delete_message_error_msg: '',
      page_limit: 5,
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
    this.get_all_message()
  },
  methods: {
    get_date: function (date) {
      let temp = new Date(date)
      return temp.toLocaleString()
    },
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
    want_reply: function (Id) {
      this.reply_comment_id = Id
      this.$root.$emit('bv::show::modal', 'reply-popup')
    },
    get_all_message: function () {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'get-course-comments/',
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
            that.get_all_message_test = true
            that.get_all_message_error_msg = that.$t('error.object_not_found')
          } else if (
            error.response.data.message === 'Commenting is not allowed.'
          ) {
            that.can_comment = false
          }
        })
    },
    up_vote: function (index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'up-vote-comment?' +
            'comment_id=' +
            Id
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
    up_vote_child_reply: function (index, reply_index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play' +
            '/up-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.message_list[index].replies[reply_index].up_votes =
              response.data.up_votes
            that.message_list[index].replies[reply_index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.message_list[index].replies[reply_index].up_votes =
              response.data.up_votes
            that.message_list[index].replies[reply_index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    modal_up_vote_reply: function (reply_index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'up-vote-comment?' +
            'comment_id=' +
            Id
        )
        .then(function (response) {
          if (response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          } else if (response.data.message === 'Access denied.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.access_denied')
          } else if (response.data.up_voted === true) {
            that.replies[reply_index].up_votes = response.data.up_votes
            that.replies[reply_index].up_voted = true
          } else if (response.data.up_voted === false) {
            that.replies[reply_index].up_votes = response.data.up_votes
            that.replies[reply_index].up_voted = false
          }
        })
        .catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error.response.data.message
        })
    },
    down_vote: function (index, Id) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            Id
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
    down_vote_child_reply: function (index, reply_index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].replies[reply_index].down_votes =
              response.data.down_votes
            that.message_list[index].replies[reply_index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.message_list[index].replies[reply_index].down_votes =
              response.data.down_votes
            that.message_list[index].replies[reply_index].down_voted = false
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
    modal_down_vote_reply: function (reply_index, msgCommentId) {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/play/' +
            'down-vote-comment?' +
            'comment_id=' +
            msgCommentId
        )
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.replies[reply_index].down_votes = response.data.down_votes
            that.replies[reply_index].down_voted = true
          } else if (response.data.down_voted === false) {
            that.replies[reply_index].down_votes = response.data.down_votes
            that.replies[reply_index].down_voted = false
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
          'http://localhost/api/v1/courses/forestage/play/' + 'get-replies/',
          {
            params: {
              comment_id: commentId,
              page_limit: that.modal_page_limit,
              page: that.modal_page
            }
          }
        )
        .then(function (response) {
          that.replies = response.data.content
          that.modal_rows = response.data.count
        })
    },
    delete_comment: function (commentId) {
      let that = this
      axios
        .post(
          'http://localhost/api/v1/courses/forestage/play' + '/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            alert(that.$t('prompt.object_deleted'))
            that.get_all_message()
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
          'http://localhost/api/v1/courses/forestage/play' + '/delete-comment/',
          qs.stringify({
            comment_id: commentId
          })
        )
        .then(function (response) {
          if (response.data.message === 'Object deleted.') {
            alert(that.$t('prompt.object_deleted'))
            that.replies.splice(index, 1)
            that.get_replies(that.get_all_reply_id)
            that.get_all_message()
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
          'http://localhost/api/v1/courses/forestage/play/add-comment/',
          qs.stringify({
            content: value,
            course_id: that.course_id
          })
        )
        .then(function (response) {
          if (response.data.message === 'Success.') {
            that.get_all_message()
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
            'http://localhost/api/v1/courses/forestage/play/add-comment/',
            qs.stringify({
              content: value,
              course_id: that.course_id,
              reply_to_id: that.reply_comment_id
            })
          )
          .then(function (response) {
            if (response.data.message === 'Success.') {
              that.get_all_message()
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
      this.get_all_message()
    }
  }
}
</script>

<style scoped>
.margin-right-1 {
  margin-right: 1rem;
}

.comment-wrap {
  word-break: normal;
  word-wrap: break-word;
}

.time-style {
  margin-right: 1rem;
  font-size: 14px;
  color: #adb5bd;
}

.time-remind {
  display: flex;
  flex-direction: row;
}

.reply-message {
  padding: 1rem 0 0 3rem;
}

.textarea-style {
  width: 93%;
  height: 70%;
  padding: 0;
  resize: none;
  border: solid 2px #ddd;
}

.textarea-style:focus {
  border: solid 2px #cce5ff;
}

.commit-button-style {
  width: 8%;
  height: 70%;
  text-align: right;
}

.all-reply {
  display: flex;
  flex-direction: row;
  padding-left: 3rem;
  font-size: 14px;
}

.look-all {
  color: #096;
  cursor: pointer;
}

.row1 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.row2 {
  display: flex;
  flex-direction: row;
}

.row3 {
  font-size: 14px;
  font-weight: bold;
  color: #999;
}

.text-align-left {
  text-align: left;
}

.message-area {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 90%;
  height: 100%;
  border-bottom: 1px solid #eee;
}

.message-list-area {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 90%;
  height: 100%;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.comment-style {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  height: 6rem;
  margin: 1rem 0.5rem 1rem 0;
}

.piece-of-message {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  height: auto;
  margin: 1rem 0.5rem 1rem 0;
}

.user-avatar {
  width: 10%;
  padding-top: 0.3rem;
  vertical-align: center;
}

.vote-style {
  width: 15px;
  height: 15px;
}

.vote-style:hover {
  filter: brightness(110%);
}

.userimg {
  width: 50px;
  height: 50px;
  margin-right: 20px;
  border-radius: 50%;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.delete-comment {
  text-align: right;
}

.add_comment {
  width: 100%;
  height: 100%;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  background-color: #cce5ff;
  border: none;
}

.message-username {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.message-list-username {
  font-size: 15px;
  font-weight: bold;
  color: #333;
}

.vip-style {
  font-size: 16px;
  font-weight: bold;
  color: rgba(255, 234, 18, 0.75);
}
</style>
