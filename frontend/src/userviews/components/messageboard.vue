<template>
  <div
    id="message-board">
    <div>
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
          :key="index"
          class="piece-of-message">
          <div id="piece-of-message">
            <b-row>
              <b-col class="text-align-left">
                <img
                  id="userimg"
                  src="../../assets/logo.png">
                {{ message_list[index-1].username }}
                <label class="time-style">&emsp;{{ message_list[index-1].created_at }}评论</label>
              </b-col>
              <b-col
                v-if="message_list[index-1].username === username"
                class="delete-comment"
                @click="delete_comment(message_list[index-1].comment_id)">
                ×
              </b-col>
            </b-row>
            <p class="message-content">{{ message_list[index-1].content }}</p>
          </div>
          <div
            id="operator">
            {{ message_list[index-1].up_votes }}
            <img
              id="praise-button"
              src="../../assets/praise.png"
              class="vote-style "
              @click="up_vote(index-1,message_list[index-1].comment_id)">
            &emsp; &emsp;{{ message_list[index-1].down_votes }}
            <img
              id="detest-button"
              src="../../assets/detest.png"
              class="vote-style "
              @click="down_vote(index-1,message_list[index-1].comment_id)">
          </div>
        </div>
      </div>
    </div>
    <div>
      <textarea
        id="input-message"
        v-model="new_msg"
        class="textarea-style"
        placeholder="请输入留言"
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
      type: String,
      default: function () {
        return 0
      }
    }
  },
  data () {
    return {
      username: '小可爱',
      new_msg: '',
      message_list: [
      ],
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
      page: 0,
      rows: 0
    }
  },
  created: function () {
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/forestage/play/get-course-comments/',
      { params: {
        course_id: that.course_id,
        page_limit: that.page_limit,
        page: that.page
      }})
      .then(function (response) {
        that.rows = response.data.count
        console.log(response)
        that.message_list = response.data.content
      }).catch(function (error) {
        that.created_test = true
        that.created_error_msg = error
      })
  },
  methods: {
    getallmessage: function () {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/get-course-comments/',
        { params: {
          course_id: that.course_id,
          page_limit: that.page_limit,
          page: that.page
        }})
        .then(function (response) {
          that.message_list = response.data.content
        }).catch(function (error) {
          that.getallmessage_test = true
          that.getallmessage_error_msg = error
        })
    },
    up_vote: function (index, msgCommentId) {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/up-vote-comment?' +
        'comment_id=' + msgCommentId)
        .then(function (response) {
          if (response.data.up_voted === true) {
            that.message_list[index].up_votes = response.data.up_votes
          } else if (response.data.up_voted === false) {
            that.message_list[index].up_votes = response.data.up_votes
          }
        }).catch(function (error) {
          that.up_vote_test = true
          that.up_vote_error_msg = error
        })
    },
    down_vote: function (index, msgCommentId) {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/down-vote-comment?' +
        'comment_id=' + msgCommentId)
        .then(function (response) {
          if (response.data.down_voted === true) {
            that.message_list[index].down_votes = response.data.down_votes
          } else if (response.data.down_voted === false) {
            that.message_list[index].down_votes = response.data.down_votes
          }
        }).catch(function (error) {
          that.down_vote_test = true
          that.down_vote_error_msg = error
        })
    },
    delete_comment: function (commentId) {
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/delete-comment?' +
        'comment_id=' + commentId)
        .then(function (response) {
          if (response.message === 'Object deleted') {
            this.getallmessage()
          } else {
            alert(response.message)
          }
        }).catch(function (error) {
          this.delete_message_test = true
          this.delete_message_error_msg = error
        })
    },
    add_comment: function () {
      const value = this.new_msg && this.new_msg.trim()
      if (!value) {
        return
      }
      axios.post('http://localhost:8000/api/v1/courses/forestage/play/add-comment?' +
        'course=' + parseInt(this.course_id),
      qs.stringify({
        content: value
      })).then(function (response) {
        if (response.message === 'Object deleted') {
          this.getallmessage()
        } else {
          alert(response.message)
        }
      }).catch(function (error) {
        this.add_message_test = true
        this.add_message_error_msg = error
      })
      this.new_msg = ''
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
    text-align: center;
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

  #userimg {
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
