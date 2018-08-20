<template>
  <body>
    <hr>
    <div style="display: flex; flex-direction: row; color: #999;">
      <div style="width: 95%;">
        <label id="list-title">{{ list_title }}</label>
      </div>
      <div style="width: 5%;">
        <label
          id="watch-more"
          @click="watch_more">更多</label>
      </div>
    </div>
    <b-container class="bv-example-row">
      <b-row>
        <b-col
          v-for="i in [0, 1, 2, 3]"
          :key="i">
          <b-card
            :img-src="courselist[i].src"
            :title="courselist[i].name"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 20rem;"
            class="mb-2"
            @click="open_detail_page(courselist[i].id)">
            <p class="card-text">
              {{ courselist[i].introduction }}
            </p>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          v-for="i in [0, 1, 2, 3]"
          :key="i">
          <b-card
            id="course-card"
            :img-src="courselist[i].src"
            :title="courselist[i].name"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 20rem;"
            class="mb-2"
            @click="open_detail_page(courselist[i].id)">
            <p class="card-text">
              {{ courselist[i].introduction }}
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
    list_title: {
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
  methods: {
    watch_more: function () {
      if (this.list_title === '免费课程') {
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
