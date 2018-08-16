<template>
  <b-modal
    ref="modal"
    :id="id"
    :title="title"
    :ok-title="ok_title"
    :cancel-title="cancel_title"
    centered>
    <p>{{ text }}</p>
  </b-modal>
</template>

<script>
export default {
  name: 'ConfirmModal',
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
  }
}
</script>

<style scoped>
  p {
    text-align: left;
  }
</style>
