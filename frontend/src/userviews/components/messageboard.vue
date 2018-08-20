<template>
  <div
    id="message-board">
    <div>
      <div class="form-style">
        <div
          v-for="msg in message_list"
          :key="msg.id"
          class="piece-of-message">
          <div id="piece-of-message">
            {{ msg.username }}
            <label class="time-style">&emsp;{{ msg.time_to_comment }}个月前</label>
            <p style="margin-bottom: 5px;">{{ msg.message_content }}</p>
          </div>
          <div
            id="operator">
            {{ msg.num_of_praise }}
            <img
              id="praise-button"
              src="../../assets/praise.png"
              class="vote-style "
              @click="msg.num_of_praise+=1">
            &emsp; &emsp;{{ msg.num_of_detest }}
            <img
              id="detest-button"
              src="../../assets/detest.png"
              class="vote-style "
              @click="msg.num_of_detest+=1">
          </div>
        </div>
      </div>
    </div>
    <div>
      <textarea
        id="input-message"
        v-model="newMsg"
        autofocus
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
export default {
  name: 'MessageBoard',
  data () {
    return {
      username: '谢逊',
      newMsg: '',
      message_list: [
        {
          id: 1,
          username: '张三丰',
          message_content: '不是谁家的粉 但觉得真的还挺好听的呀 ' +
            '毕竟是翻唱演绎 肯定会和之前不太一样的 不然就没有看点了嘛﻿',
          num_of_praise: 50,
          num_of_detest: 60,
          time_to_comment: 3
        },
        {
          id: 2,
          username: '张无忌',
          message_content: 'Gitlab服务器炸了，你们知道吗？',
          num_of_praise: 60,
          num_of_detest: 70,
          time_to_comment: 3
        },
        {
          id: 3,
          username: '周芷若',
          message_content: '這次鄧紫棋唱出自己的特色，' +
            '她在某幾個調轉了另一種唱法，讓這首歌有着另一種感覺，所以真的不應一直衹唱高音﻿',
          num_of_praise: 20,
          num_of_detest: 10,
          time_to_comment: 3
        }
      ]
    }
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
    border-radius: 20px;
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
</style>
