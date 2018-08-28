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
    <Alert
      :count_down="wrong_count_down"
      :instruction="wrong"
      variant="danger"
      @decrease="wrong_count_down-1"
      @zero="wrong_count_down=0"/>
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
import Alert from '../../components/alert'
export default {
  name: 'InputModal',
  components: {Alert},
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
      input: '',
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  methods: {
    clear_input () {
      this.input = ''
    },
    handle_ok (evt) {
      if (this.input === '') {
        evt.preventDefault()
        this.wrong = '请输入内容后提交'
        this.wrong_count_down = this.dismiss_second
      } else {
        this.$emit('click', this.input)
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
