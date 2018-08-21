<template>
  <div
    id="message-board">
    <div>
      <b-alert
        :show="test"
        variant="danger"
        dismissible
        fade
        @dismissed="showDismissibleAlert=false">
        {{ error_msg }}
      </b-alert>
      <div class="form-style">
        <div
          v-for="msg in message_list"
          :key="msg.id"
          class="piece-of-message">
          <div id="piece-of-message">
            <img
              id="userimg"
              src="../../assets/logo.png">
            {{ msg.username }}
            <label class="time-style">&emsp;{{ msg.created_at }}评论</label>
            <p style="margin-bottom: 5px;">{{ msg.content }}</p>
          </div>
          <div
            id="operator">
            {{ msg.up_votes }}
            <img
              id="praise-button"
              src="../../assets/praise.png"
              class="vote-style "
              @click="up_vote">
            &emsp; &emsp;{{ msg.down_votes }}
            <img
              id="detest-button"
              src="../../assets/detest.png"
              class="vote-style "
              @click="down_vote">
          </div>
        </div>
      </div>
    </div>
    <div>
      <textarea
        id="input-message"
        v-model="newMsg"
        class="textarea-style"
        placeholder="请输入留言"
        @keyup.enter="addmessage"/>
      <br>
      <div
        id="commit-button"
        class="commit-button-style">
        <b-button
          @click="addmessage">评论</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MessageBoard',
  data () {
    return {
      username: '谢逊',
      newMsg: '',
      message_list: [],
      test: false,
      error_msg: ''
    }
  },
  created: function () {
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/forestage/play/get-course-comments?course_id=1')
      .then(function (response) {
        that.message_list = response.data.content
      }).catch(function (error) {
        that.test = true
        this.error_msg = error
      })
  },
  methods: {
    addmessage: function () {
      var value = this.newMsg && this.newMsg.trim()
      this.message_list.push({
        username: this.username,
        message_content: value,
        num_of_praise: 0,
        num_of_detest: 0})
      this.newMsg = ''
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/add-comment?course_id=1')
        .then(function (response) {
          // console.log(response)
        }).catch(function (error) {
          this.test = true
          this.error_msg = error
        })
    },
    up_vote: function () {
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/up-vote-comment?comment_id=1')
        .then(function (response) {
          // console.log(response)
        }).catch(function (error) {
          this.test = true
          error.msg = error
        })
    },
    down_vote: function () {
      axios.get('http://localhost:8000/api/v1/courses/forestage/play/down-vote-comment?comment_id=1')
        .then(function (response) {
          // console.log(response)
        }).catch(function (error) {
          this.test = true
          this.error_msg = error
        })
    }
  }
}
</script>

<style>
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
</style>
