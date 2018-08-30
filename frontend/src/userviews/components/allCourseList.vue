<template>
  <div>
    <div class="body container">
      <div class="title">
        <h4>{{ page_title }}</h4>
        <div class="another-page">
          <simple-line-icons
            style="display: inline;"
            icon="arrow-right"
            color="#FCE1E5"
            class="icon"
            size="large"/>
          <span @click="to_another_page">{{ another_page_title }}</span>
        </div>
      </div>
      <div
        v-for="course in course_list"
        id="course-list"
        :key="course.course_id">
        <div
          class="course"
          @click="open_detail_page(course.course_id)">
          <img
            :src="$store.state.address + course.thumbnail"
            class="image">
          <div class="introduction wrap-style">
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
    another_page_title: {
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
  methods: {
    /**
     * 页面跳转
     * 打开课程详情页面
     * @params id 课程id
     * 跳转将课程id传给课程详情页面 */
    open_detail_page: function (id) {
      this.$router.push({ name: 'CourseDetail', query: { course_id: id } })
    },
    /**
     * 改变页码
     * @params page 分页器当前页码
     * 发送给父组件该分页组件的页码值
     * 传入函数：change_page
     * */
    change_page: function (page) {
      this.$emit('change_page', page)
    },
    /**
     * */
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
    },
    to_another_page: function () {
      this.$emit('to_another_page')
    }
  }
}
</script>

<style scoped>
p {
  text-indent: 2rem;
}

.container {
  padding: 20px 0 20px 0;
}

.title {
  display: flex;
  justify-content: space-between;
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

.wrap-style {
  word-break: break-word;
}

span {
  cursor: pointer;
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
