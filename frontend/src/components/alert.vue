<template>
  <div class="alert-div">
    <b-alert
      :show="count_down"
      :variant="variant"
      class="my-alert"
      dismissible
      @dismissed="dismiss"
      @dismiss_count_down="count_down_changed">
      {{ instruction }}
    </b-alert>
  </div>
</template>

<script>
export default {
  name: 'Alert',
  /**
   * variant: string, 警告框的颜色
   * count_down: number, 距离警告框关闭的时间
   * instruction: string, 警告框上的提示信息
   */
  props: {
    variant: {
      type: String,
      default: 'danger'
    },
    count_down: {
      type: Number,
      default: 0
    },
    instruction: {
      type: String,
      default: ''
    }
  },
  methods: {
    /**
     * 该函数实现倒计时功能，
     * 每隔一秒触发一次decrease函数，直至为0。
     */
    count_down_changed: function () {
      const that = this
      let time = setInterval(function () {
        this.$emit('decrease')
        if (that.val === 0) {
          clearInterval(time)
        }
      }, 1000)
    },
    /**
     * 该函数关闭模态框，
     * 触发zero函数。
     */
    dismiss: function () {
      this.$emit('zero')
    }
  }
}
</script>

<style scoped>
.alert-div {
  position: fixed;
  top: 25%;
  left: 45%;
}
</style>
