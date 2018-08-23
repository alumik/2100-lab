<template>
  <body>
    <div class="navbar-style">
      <UserNavbar/>
      <b-alert
        :show="created_test"
        variant="danger"
        dismissible
        @dismissed="created_test = false">
        {{ created_error_msg }}
      </b-alert>
    </div>
    <div class="homepage-container">
      <div class="carousel-container">
        <b-carousel
          id="carousel"
          :interval="2000"
          controls
          indicators
          img-responsive
          background="#ababab"
        >
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-1"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=30"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-2"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=31"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-3"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=32"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-4"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=33"/>
        </b-carousel>
      </div>
      <div class="recommend-list">
        <RecommendList
          :courselist="freecourselist"
          course_type="free"/>
        <RecommendList
          :courselist="paidcourselist"
          course_type="paid"/>
      </div>
    </div>
  </body>
</template>

<script>
import UserNavbar from '../components/navbar'
import RecommendList from '../components/recommendList'
import axios from 'axios'

export default {
  name: 'Homepage',
  components: {
    UserNavbar,
    RecommendList
  },
  data () {
    return {
      test: false,
      err_msg: '',
      freecourselist: [],
      paidcourselist: [],
      created_test: false,
      created_error_msg: ''
    }
  },
  created: function () {
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/forestage/course/get-recent-courses')
      .then(function (response) {
        that.freecourselist = response.data.free_courses
        that.paidcourselist = response.data.paid_courses
      }).catch(function (error) {
        that.created_test = true
        that.created_error_msg = error
      })
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .homepage-container {
    margin-right: 0;
    margin-left: 0;
    border-width: 0.2rem;
  }

  .navbar-style {
    position: fixed;
    z-index: 999;
    width: 100%;
  }

  .recommend-list {
    width: 100%;
    padding: 1rem;
    margin: 0;
  }
</style>
