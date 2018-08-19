<template>
  <body class="container-style">
    <div class="list-title">
      <div class="title-style">
        <label>{{ list_title }}</label>
      </div>
      <div class="watch-more">
        <label @click="watch_more">更多</label>
      </div>
    </div>
    <div class="course-list-style">
      <div
        v-for="course in courselist"
        :key="course.id"
        :gutter="40"
        class="panel-group">
        <div
          class="card-panel-col">
          <div
            class="card-panel"
            @click="handleSetLineChartData('skys')">
            <div class="card-panel-icon-wrapper icon-sky">
              <img
                :src="course.src"
                class="card-panel-icon"
                @click="open_detail_page(course.id)"
              >
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">{{ course.name }}</div>
              <div class="card-panel-text card-panel-course-description">
                {{ course.introduction }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  name: 'FreeRecommendList',
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
    handleSetLineChartData (type) {
      this.$emit('handleSetLineChartData', type)
    },
    open_detail_page: function (id) {
      this.$router.push({name: 'CourseDetail', query: {course_id: id}})
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .container-style {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    padding: 0;
    margin: 0;
    text-align: left;
  }

  .list-title {
    display: flex;
    width: 100%;
    height: 30px;
    margin-top: 10px;
    margin-left: 15px;
    font-size: 16px;
    color: #adb5bd;
  }

  .title-style {
    width: 50%;
    text-align: left;
  }

  .course-list-style {
    display: flex;
    flex-direction: row;
    flex-grow: 1;
    width: 100%;
  }

  .watch-more {
    width: 47%;
    text-align: right;
  }

  .panel-group {
    display: flex;
    flex-grow: 1;
    margin-left: 15px;

    .card-panel-col {
      margin-bottom: 32px;
    }

    .card-panel {
      display: flex;
      flex-direction: column;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-size: 12px;
      cursor: pointer;
      border: 1px solid #ebebeb;
      box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);

      img {
        width: 210px;
        height: 150px;
      }

      .card-panel-icon-wrapper {
        padding: 3px;
        margin: 4px;
        border-radius: 6px;
        transition: all 0.38s ease-out;
      }

      .icon-sky {
        color: #d1ecf1;
      }

      &:hover {
        .icon-sky {
          background: #d1ecf1;
        }
      }

      .card-panel-icon {
        font-size: 48px;
      }

      .card-panel-description {
        float: right;
        margin: 26px;
        font-weight: bold;

        .card-panel-text {
          margin-bottom: 12px;
          font-size: 16px;
          line-height: 18px;
          color: rgba(0, 0, 0, 0.45);
        }

        .card-panel-course-description {
          font-size: 14px;
          color: #000;
          text-align: left;
        }

        .card-panel-num {
          font-size: 20px;
        }
      }
    }
  }
</style>
