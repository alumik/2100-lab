<template>
  <body>
    <UserNavbar/>
    <b-alert
      :show="created_test"
      variant="danger"
      dismissible
      @dismissed="created_test = false">
      {{ created_error_msg }}
    </b-alert>
    <b-alert
      :show="carousel_test"
      variant="danger"
      dismissible
      fade
      @dismissed="carousel_test=false">
      {{ carousel_error_msg }}
    </b-alert>
    <div class="homepage-container">
      <div class="carousel-container">
        <b-carousel
          id="carousel"
          :interval="2000"
          controls
          indicators
          img-responsive
        >
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-1"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=60"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-2"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=70"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-3"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=80"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-4"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=90"/>
        </b-carousel>
      </div>
      <div class="recommend-list">
        <RecommendList
          :courselist="freecourselist"
          course_type="free"
          class="list-style"/>
        <hr>
        <RecommendList
          :courselist="paidcourselist"
          class="paid-recommend"
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
      carousellist: [],
      carouselnum: 0,
      freecourselist: [],
      paidcourselist: [],
      created_test: false,
      created_error_msg: '',
      carousel_test: false,
      carousel_error_msg: ''
    }
  },
  created: function () {
    let that = this
    axios
      .get(
        'http://localhost:8000/api/v1/courses/forestage/course/get-recent-courses'
      )
      .then(function (response) {
        // console.log(response.data.free_courses)
        that.freecourselist = response.data.free_courses
        that.paidcourselist = response.data.paid_courses
      })
      .catch(function (error) {
        that.created_test = true
        that.created_error_msg = error
      })
    axios
      .get('http://localhost:8000/api/v1/courses/forestage/main/get-heroes/')
      .then(function (response) {
        that.carousellist = response.content
        that.carouselnum = response.count
      })
      .catch(function (error) {
        that.carousel_test = true
        that.carousel_error_msg = error
      })
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.list-style {
  margin: 3rem 0;
}

.paid-recommend {
  margin-top: 3.5rem;
}

.homepage-container {
  margin-right: 0;
  margin-left: 0;
  border-width: 0.2rem;
}

.recommend-list {
  width: 100%;
  padding: 3rem;
  margin: 0;
}
</style>
