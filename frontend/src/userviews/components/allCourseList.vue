<template>
  <div>
    <div class="body container">
      <h4>{{ page_title }}</h4>
      <div
        v-for="course in course_list"
        id="course-list"
        :key="course.course_id">
        <div
          class="course"
          @click="open_detail_page(course.course_id)">
          <img
            :src="example_src"
            class="image">
          <div class="introduction">
            <h5>{{ course.title }}</h5>
            <p id="text-one">
              {{ compute_message(course.description, 120) }}
            </p>
            <p id="text-two">
              {{ compute_message(course.description, 12) }}
            </p>
          </div>
        </div>
      </div>
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
      default: 15
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
      this.$router.push({ name: 'CourseDetail', query: { course_id: id } })
    },
    change_page: function (page) {
      this.$emit('change_page', page)
    },
    compute_message: function (message, val) {
      if (message) {
        if (message.length > val) {
          return message.slice(0, val) + '...'
        } else {
          return message
        }
      } else {
        return ''
      }
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px 0 20px 0;
}

h4 {
  margin: 20px 0 20px 0;
  text-align: left;
  vertical-align: center;
}

.course {
  display: flex;
  align-items: center;
  padding: 20px 0 20px 0;
  cursor: pointer;
  border-top: 1px solid #e6e6e6;
  border-bottom: 1px solid #e6e6e6;
}

.image {
  width: 300px;
  height: 200px;
  margin-right: 50px;
  overflow-x: hidden;
}

.introduction {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 900px;
  height: 200px;
  text-align: left;
}

h5,
#text-one {
  padding: 2px 0 2px 0;
  margin: 20px;
}

#text-two {
  display: none;
}

@media (max-width: 800px) {
  .course {
    height: 100px;
  }

  .image {
    width: 120px;
    height: 80px;
    margin-left: 5px;
  }

  .introduction {
    justify-content: center;
    width: 220px;
    height: 100px;
    text-align: left;
  }

  h5 {
    width: 240px;
    margin: 3px 2px 3px 2px;
  }

  #text-two {
    display: block;
    width: 240px;
    margin: 3px 2px 3px 2px;
  }

  #text-one {
    display: none;
  }
}
</style>
