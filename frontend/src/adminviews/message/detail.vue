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
            placeholder="请输入你要回复的内容"/>
          <button
            v-b-modal.delete
            type="button"
            class="btn btn-lg">
            删除留言
          </button>
          <ConfirmModal
            id="delete"
            title="确认删除"
            text="您确定要删除此条留言吗？"/>
        </div>
      </div>
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
export default {
  name: 'MessageDetail',
  components: { DetailTable, Basic, InputModal, ConfirmModal },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '留言管理',
        href: '/admin/message'
      }, {
        text: this.$route.query.message_id,
        active: true
      }],
      titles: ['留言日期', '用户', '课程代码', '课程名', '状态', '内容'],
      message: [ '2018-08-10', '小红', 'SOFT1', '计算机', '已删除', '很好' ]
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
</style>
