<template>
  <body>
    <hr>
    <b-container class="text-color">
      <b-row>
        <b-col
          cols="8"
          class="text-align-left">
          <label id="list-title">{{ course_type === 'free' ? '免费课程':'付费课程' }}</label>
        </b-col>
        <b-col
          class="text-align-right">
          <label
            id="watch-more"
            @click="watch_more">更多</label>
        </b-col>
      </b-row>
    </b-container>
    <div
      id="course-list"
      class="course-list-style">
      <b-container class="bv-example-row">
        <b-form-row>
          <b-col
            v-for="course in courselist"
            :key="course.course_id"
            class="col-style col-card-style">
            <b-card
              :img-src="example_src"
              img-alt="Img"
              img-top>
              <p style="height: 2.5rem;">
                {{ course.title }}
              </p>
              <p class="card-text card-text-height">
                {{ course.description.substring(0,30) }}
              </p>
            </b-card>
          </b-col>
        </b-form-row>
      </b-container>
    </div>
  </body>
</template>

<script>
export default {
  name: 'RecommendList',
  props: {
    course_type: {
      type: String,
      default: function () {
        return ''
      }
    },
    courselist: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  data () {
    return {
      example_src: 'https://picsum.photos/400/300/?image=790'
    }
  },
  methods: {
    watch_more: function () {
      if (this.course_type === 'free') {
        this.$router.push({name: 'AllFreeCourse'})
      } else {
        this.$router.push({name: 'AllPaidCourse'})
      }
    },
    open_detail_page: function (id) {
      this.$router.push({name: 'CourseDetail', query: {course_id: id}})
    }
  }
}
</script>

<style>
  .text-align-right {
    text-align: right;
  }

  .text-align-left {
    text-align: left;
  }

  .text-color {
    color: #999;
  }

  .col-card-style {
    width: 16rem;
    min-width: 16rem;
    max-width: 16rem;
    height: 22.5rem;
    min-height: 22.5rem;
    max-height: 22.5rem;
  }

  .col-style {
    flex: 1 0 20%;
    padding: 0;
    margin: 0.7rem;
    text-align: center;
  }

  .card-text-height {
    height: 5rem;
  }

  #course-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .course-list-style {
    margin: 0;
  }
</style>
