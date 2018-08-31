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
  /**
   * id: string, 模态框id
   * title: string, 模态框标题
   * ok_title: string, 确认按钮标题
   * cancel_title: string, 取消按钮标题
   * placeholder: string 占位符内容
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
  /**
   * @returns {{
   * input: string, 模态框中输入内容
   * dismiss_second: number,
   * wrong_count_down: number,
   * wrong: string
   * Alert组件所需数据
   * }}
   */
  data () {
    return {
      input: '',
      dismiss_second: 5,
      wrong_count_down: 0,
      wrong: ''
    }
  },
  methods: {
    /**
     * 该函数清空输入框中内容
     */
    clear_input () {
      this.input = ''
    },
    /**
     * 该函数接受一个事件参数，处理确认按钮请求，判断输入内容是否为空，
     * 输入内容为空，提示错误，
     * 输入内容不为空，触发click函数，关闭模态框
     * @param evt
     */
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
    /**
     * 该函数关闭模态框并清空输入内容
     */
    handle_submit () {
      this.$refs.modal.hide()
      this.clear_input()
    }
  }
}
</script>
