<template>
  <div
    id="message-board"
    class="container msgboard-style">
    <div
      class="panel panel-style">
      <ul class="form-style">
        <li
          v-for="msg in message_list"
          :key="msg.id"
          class="form-control piece-of-message">
          <div id="message">
            <h5 style="font-weight: bold;">{{ msg.username }}</h5>
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
        class="textarea-style"
        placeholder="请输入留言"
        @keyup.enter="addmessage"/>
      <br>
      <div
        id="commit-button"
        class="commit-button-style">
        <button
          class="btn btn-primary btn-style"
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
          id: 1,
          username: '张三丰',
          message_content: '今天天气不错',
          num_of_praise: 50,
          num_of_detest: 60
        },
        {
          id: 2,
          username: '张无忌',
          message_content: 'Gitlab服务器炸了，你们知道吗？',
          num_of_praise: 60,
          num_of_detest: 70
        },
        {
          id: 3,
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
  .msgboard-style {
    width: 100%;
    height: 100%;
    text-align: center;
  }

  .textarea-style {
    width: 100%;
    height: 100%;
  }

  .commit-button-style {
    width: 100%;
    text-align: right;
  }

  .btn-style {
    width: 10%;
    margin-top: 10px;
  }

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
    width: 98%;
    height: 50%;
    margin: 10px;
    text-align: left;
  }

  .panel-style {
    width: 100%;
    height: 80%;
  }
</style>
