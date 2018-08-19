<template>
  <Basic
    :items="items"
    class="special">
    <SyncPictureBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import SyncPictureBasic from './components/synchronization_basic'
export default {
  name: 'SyncPicture',
  components: {SyncPictureBasic, Basic},
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin'
        }, {
          text: '课程管理',
          href: '/admin/course'
        }, {
          text: '新增课程',
          href: '/admin/course/creation'
        }, {
          text: '音图片同步',
          active: true
        }]
    }
  }
}
</script>

<style scoped>
  .special {
    min-width: 1300px;
  }

  .my-content {
    margin: 40px;
    text-align: left;
  }
</style>
