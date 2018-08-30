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
            :caption="carousellist[0] ? carousellist[0].caption : ''"
            :img-src="carousellist[0] ? $store.state.address+
            carousellist[0].image : '//user-assets.sxlcdn.com/images/170814/FpZwQkvM2TZeBBwl21F5kdNuUANA.jpg?' +
            'imageMogr2/strip/thumbnail/2000x1500>/quality/90!/interlace/1/format/jpeg'"
            img-width="1024"
            img-height="250"
            class="height-change"
            name="carousel-pic-1"/>
          <b-carousel-slide
            :caption="carousellist[1] ? carousellist[1].caption : ''"
            :img-src="carousellist[1] ? $store.state.address+
            carousellist[1].image : 'http://user-assets.sxlcdn.com/images/170814/FqT_2HP4cJvS2AYN61fz8lcVq8qZ.GIF?'+
            'imageMogr2/strip/thumbnail/2000x1500%3E/quality/90!/format/gif'"
            img-width="1024"
            img-height="250"
            class="height-change"
            name="carousel-pic-2"/>
          <b-carousel-slide
            :caption="carousellist[2] ? carousellist[2].caption : ''"
            :img-src="carousellist[2] ? $store.state.address+
            carousellist[2].image : '//user-assets.sxlcdn.com/images/170814/FsnphZv9Oyrrb3jzfey280s07VvC.jpg?' +
            'imageMogr2/strip/thumbnail/1200x9000>/quality/90!/interlace/1/format/jpeg'"
            img-width="1024"
            img-height="250"
            class="height-change"
            name="carousel-pic-3"/>
          <b-carousel-slide
            :caption="carousellist[3] ? carousellist[3].caption : ''"
            :img-src="carousellist[3] ? $store.state.address+
            carousellist[3].image : '//user-assets.sxlcdn.com/images/170814/Fj7zqHIvtHv87AlY63ZmFKPf-lB_.jpg?' +
            'imageMogr2/strip/thumbnail/1200x9000>/quality/90!/interlace/1/format/jpeg'"
            img-width="1024"
            img-height="250"
            class="height-change"
            name="carousel-pic-4"/>
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
    <div class="footer">
      <p class="text-center">
        --- 2100实验室 ---
      </p>
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
        'http://localhost/api/v1/courses/forestage/course/get-recent-courses'
      )
      .then(function (response) {
        that.freecourselist = response.data.free_courses
        that.paidcourselist = response.data.paid_courses
      })
      .catch(function (error) {
        that.created_test = true
        that.created_error_msg = error
      })
    axios
      .get('http://localhost/api/v1/courses/forestage/main/get-heroes/')
      .then(function (response) {
        that.carousellist = response.data.content
        that.carouselnum = response.data.count
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

.height-change {
  max-height: calc(0.382 * 100vw);
}
</style>
