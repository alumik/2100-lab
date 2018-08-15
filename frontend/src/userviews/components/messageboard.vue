<template>
  <div
    id="message-board"
    style="height: 100%; width: 100%;"
    class="container">
    <div
      class="panel"
      style="height: 80%; width: 100%;">
      <ul style="width: 100%; padding: 0; border: 1px solid #c6c8ca; text-align: center;">
        <li
          v-for="msg in message_list"
          :key="msg"
          class="form-control"
          style="text-align: left; height:50%; width: 98%; margin: 10px;">
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
      class="container"
      style="marigin-left: 80px; height: 20%; height: 100%; border: 1px solid #c6c8ca; padding: 5px 10px;">
      <input
        v-model="newMsg"
        autofocus
        class="form-control"
        placeholder="请输入留言"
        @keyup.enter="addmessage">
      <br>
      <button
        class="btn btn-primary btn-block"
        @click="addmessage">提交</button>
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
      this.message_list.push({ username: this.username,
        message_content: value,
        num_of_praise: 0,
        num_of_detest: 0})
      this.newMsg = ''
    }
  }
}
</script>

<style>
</style>
