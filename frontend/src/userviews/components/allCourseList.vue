<template>
  <div>
    <UserNavbar/>
    <div class="title-style">
      <h2>{{ page_title }}</h2>
    </div>
    <div
      id="course-list"
      class="bv-example-row course-list-style">
      <b-card-group
        v-for="course in course_list"
        :key="course"
        deck
        class="mb-3 b-card-group-style">
        <b-card
          :header="course.name"
          border-variant="primary"
          header-bg-variant="primary"
          header-text-variant="white"
          align="center">
          <div class="card-content">
            <div class="course-img-style">
              <b-img
                :src="course.src"
                fluid
                thumbnail
                alt="Responsive image Thumbnail"
                class="img-thumbnail card-image"
              />
            </div>
            <div class="introduction">
              &emsp; &emsp;{{ course.introduction }}
            </div>
          </div>
        </b-card>
      </b-card-group>
    </div>
    <div class="pagination-style">
      <Pagination
        :rows="rows"
        :perpage="perpage"/>
    </div>
  </div>
</template>

<script>
import UserNavbar from './navbar'
import Pagination from '../../components/pagination'

export default {
  name: 'AllCourseList',
  components: {
    UserNavbar,
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
    }
  },
  data () {
    return {
      rows: 20,
      perpage: 3,
      cards_per_page: 18
    }
  },
  methods: {
  }
}
</script>

<style>
  .title-style {
    margin-top: 30px;
    margin-left: 60px;
    text-align: left;
  }

  .card-content {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .introduction {
    width: 40%;
    height: 100%;
    margin-left: 10px;
    text-align: left;
  }

  #course-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .card-image {
    width: 100%;
    height: 100%;
    padding: 10px;
    border: 2px solid #b8daff;
  }

  .course-list-style {
    margin: 30px 0;
  }

  .b-card-group-style {
    width: 30%;
    margin: 10px;
  }

  .course-img-style {
    width: 50%;
    height: 100%;
  }

  .pagination-style {
    display: flex;
    justify-content: center;
  }
</style>
