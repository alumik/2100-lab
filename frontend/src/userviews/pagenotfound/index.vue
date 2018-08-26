<template>
  <Basic>
    <div
      id="pagenotfound">
      <div id="gif">
        <img src="../../assets/404.gif">
      </div>
      <div id="remind">
        <h4>Oops! 您访问的页面不存在</h4>
        <h4>如有问题请联系客服：15222276167</h4>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import $ from 'jquery'

$(document).ready(function (e) {
  if (window.history && window.history.pushState) {
    $(window).on('popstate', function () {
      window.history.pushState('forward', null, '/')
      location.reload()
      window.history.forward(1)
    })
  }
  window.history.pushState('forward', null, '/404')
  window.history.forward(1)
})

export default {
  name: 'BurnedCourse',
  components: {
    Basic
  }
}
</script>
