<template>
  <div>
    <div
      id="page-title"
      class="title-style">
      <h5>{{ page_title }}</h5>
    </div>
    <div
      id="course-list"
      class="bv-example-row course-list-style">
      <b-container class="bv-example-row">
        <b-row>
          <b-col
            v-for="course in course_list"
            :key="course.course_id"
            class="col-style">
            <b-card
              id="course-img"
              :img-src="example_src"
              :title="course.title"
              img-alt="Image"
              img-top
              tag="article"
              class="mb-2 width-style"
              @click="open_detail_page(course.course_id)">
              <p class="card-text">
                {{ course.description?course.description.substring(0,20):'' }}
              </p>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div class="pagination-style">
      <Pagination
        id="pagination"
        :rows="rows"
        :perpage="page_limit"
        @change="change_page"/>
    </div>
  </div>
</template>

<script>
import Pagination from '../../components/pagination'

export default {
  name: 'AllCourseList',
  components: {
    Pagination
  },
  props: {
    page_title: {
      type: String,
      default: ''
    },
    course_list: {
      type: Array,
      default: function () {
        return []
      }
    },
    page_limit: {
      type: Number,
      default: 10
    },
    page: {
      type: Number,
      default: 1
    },
    rows: {
      type: Number,
      default: 0
    }
  },
  data () {
    return {
      example_src: 'https://picsum.photos/400/300/?image=32'
    }
  },
  methods: {
    open_detail_page: function (id) {
      this.$router.push({name: 'CourseDetail', query: {course_id: id}})
    },
    change_page: function (page) {
      this.$emit('change_page', page)
    }
  }
}
</script>

<style>
  .title-style {
    margin-top: 30px;
    margin-left: 60px;
    text-align: left;
  }

  #course-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .course-list-style {
    margin: 30px 0;
  }

  .pagination-style {
    display: flex;
    justify-content: center;
  }

  .width-style {
    min-width: 10rem;
    max-width: 20rem;
  }

  .col-style {
    flex: 1 0 33%;
    margin-bottom: 20px;
  }
</style>
