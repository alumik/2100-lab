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
    count_down_changed: function () {
      const that = this
      let time = setInterval(function () {
        this.$emit('decrease')
        if (that.val === 0) {
          clearInterval(time)
        }
      }, 1000)
    },
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
