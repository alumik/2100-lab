<template>
  <div
    id="message-board"
    style="height: 100%; width: 100%; text-align: center;"
    class="container">
    <div
      class="panel"
      style="height: 80%; width: 100%;">
      <ul class="form-style">
        <li
          v-for="msg in message_list"
          :key="msg"
          class="form-control piece-of-message">
          <div id="message">
            <h style="font-weight: bold;">{{ msg.username }}</h>
            留言：{{ msg.message_content }}
          </div>
          <div
            id="operator"
            style="text-align: right;">
            {{ msg.num_of_praise }}
            <b-button @click="msg.num_of_praise+=1">赞</b-button>
            &emsp; &emsp;{{ msg.num_of_detest }}
            <b-button @click="msg.num_of_detest+=1">踩</b-button>
          </div>
        </li>
      </ul>
    </div>
    <div
      class="container leave-message">
      <textarea
        v-model="newMsg"
        autofocus
        style="width: 100%; height:100%;"
        placeholder="请输入留言"
        @keyup.enter="addmessage"/>
      <br>
      <div
        id="commit-button"
        style="width: 100%; text-align: right;">
        <button
          class="btn btn-primary"
          style="width: 10%; margin-top: 10px;"
          @click="addmessage">提交</button>
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
          username: '张三丰',
          message_content: '今天天气不错',
          num_of_praise: 50,
          num_of_detest: 60
        },
        {
          username: '张无忌',
          message_content: 'Gitlab服务器炸了，你们知道吗？',
          num_of_praise: 60,
          num_of_detest: 70
        },
        {
          username: '周芷若',
          message_content: '我想吃糖~',
          num_of_praise: 20,
          num_of_detest: 10
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
  .leave-message {
    width: 100%;
    height: 20%;
    padding: 5px 10px;
    margin-left: 0;
    border: 1px solid #c6c8ca;
  }

  .form-style {
    width: 100%;
    padding: 0;
    text-align: center;
    border: 1px solid #c6c8ca;
  }

  .piece-of-message {
    text-align: left;
    height:50%;
    width: 98%;
    margin: 10px;
  }
</style>
