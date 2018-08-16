<template>
  <b-modal
    ref="modal"
    :id="id"
    :title="title"
    :ok-title="ok_title"
    :cancel-title="cancel_title"
    centered
    @ok="handle_ok"
    @shown="clear_input">
    <form @submit.stop.prevent="handle_submit">
      <textarea
        v-model="input"
        :placeholder="placeholder"
        class="form-control"
        rows="3"/>
    </form>
  </b-modal>
</template>

<script>
export default {
  name: 'InputModal',
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
      default: '保存'
    },
    cancel_title: {
      type: String,
      default: '关闭'
    },
    placeholder: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      input: ''
    }
  },
  methods: {
    clear_input () {
      this.input = ''
    },
    handle_ok (evt) {
      if (this.input === '') {
        evt.preventDefault()
        alert('请输入内容后提交')
      } else {
        this.handle_submit()
      }
    },
    handle_submit () {
      this.$refs.modal.hide()
      this.clear_input()
    }
  }
}
</script>
