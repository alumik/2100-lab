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
    <b-container class="bv-example-row">
      <b-row>
        <b-col
          v-for="course in courselist"
          :key="course.course_id"
          class="col-style">
          <b-card
            id="course-card"
            :img-src="course.thumbnail"
            :title="course.title"
            img-alt="Image"
            img-top
            tag="article"
            class="mb-2 width-style"
            @click="open_detail_page(course.course_id)">
            <p class="card-text">
              {{ course.description.substring(0,30) }}
            </p>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
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
      example_src: 'https://picsum.photos/400/300/?image=32'
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
  .col-style {
    margin-bottom: 20px;
  }

  .text-align-right {
    text-align: right;
  }

  .text-align-left {
    text-align: left;
  }

  .text-color {
    color: #999;
  }

  .width-style {
    min-width: 10rem;
    max-width: 20rem;
  }
</style>
