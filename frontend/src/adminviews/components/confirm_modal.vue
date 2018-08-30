<template>
  <b-modal
    ref="modal"
    :id="id"
    :title="title"
    :ok-title="ok_title"
    :cancel-title="cancel_title"
    centered
    @ok="click_ok">
    <p>{{ text }}</p>
  </b-modal>
</template>

<script>
export default {
  name: 'ConfirmModal',
  /**
   * id: string, 模态框id
   * title: string, 模态框标题
   * ok_title: string, 确认按钮标题
   * cancel_title: string, 取消按钮标题
   * text: string 模态框内内容
   */
  props: {
    id: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
    ok_title: {
      type: String,
      default: '确认'
    },
    cancel_title: {
      type: String,
      default: '取消'
    },
    text: {
      type: String,
      default: ''
    }
  },
  methods: {
    /**
     * 该函数处理确认按钮事件，
     * 触发click事件，关闭模态框。
     */
    click_ok: function () {
      this.$emit('click')
      this.$refs.modal.hide()
    }
  }
}
</script>

<style scoped>
p {
  text-align: left;
}
</style>
