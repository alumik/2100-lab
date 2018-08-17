<template>
  <body>
    <el-row
      :gutter="40"
      class="panel-group list-title">
      <div>{{ list_title }}</div>
      <b-button
        class="watch-more"
        @click="watchmore">查看更多</b-button>
    </el-row>
    <div class="course-list-style">
      <el-row
        v-for="course in courselist"
        :key="course"
        :gutter="40"
        class="panel-group">
        <el-col
          :xs="12"
          :sm="12"
          :lg="6"
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
              <div class="card-panel-text">course.name</div>
              <div class="card-panel-text card-panel-course-description">
                {{ course.introduction }}
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
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
    watchmore: function () {
      if (this.list_title === '免费课程列表') {
        this.$router.push({name: 'AllFreeCourse'})
      } else {
        this.$router.push({name: 'AllPaidCourse'})
      }
    },
    handleSetLineChartData (type) {
      this.$emit('handleSetLineChartData', type)
    },
    open_detail_page: function (id) {
      this.$router.push({name: 'CourseDetail', params: {course_id: id}})
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .list-title {
    margin-left: 10px;
    font-size: 20px;
    font-weight: bold;
    color: #ff7f50;
    text-shadow: 2px 2px 2px #888;
    box-shadow: 10px 10px 5px #888;
  }

  .course-list-style {
    display: flex;
    flex-direction: row;
  }

  .watch-more {
    margin-left: 10px;
    color: #deb887;

    &:hover {
      color: #ff7f50;
      text-decoration: none;
    }
  }

  .panel-group {
    display: flex;
    flex-grow: 1;
    margin-top: 18px;

    .card-panel-col {
      margin-bottom: 32px;
    }

    .card-panel {
      position: relative;
      display: flex;
      flex-direction: column;
      width: 240px;
      height: 280px;
      margin: 10px;
      overflow: hidden;
      font-size: 12px;
      color: #666;
      cursor: pointer;
      background: #deb887;
      border-color: #deb887;
      box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);

      img {
        width: 180px;
        height: 100px;
      }

      .card-panel-icon-wrapper {
        float: none;
        padding: 16px;
        margin: 14px 14px 14px 14px;
        border-radius: 6px;
        transition: all 0.38s ease-out;
      }

      .icon-sky {
        color: #40c9c6;
      }

      .icon-cheek {
        color: #f4516c;
      }

      .icon-sea {
        color: #00f;
      }

      .icon-apple {
        color: #f00;
      }

      .icon-orange {
        color: #d2691e;
      }

      &:hover {
        .card-panel-icon-wrapper {
          color: #fff;
        }

        .icon-sky {
          background: #40c9c6;
        }

        .icon-cheek {
          background: #f4516c;
        }

        .icon-sea {
          background: #00f;
        }

        .icon-apple {
          background: #f00;
        }

        .icon-orange {
          background: #d2691e;
        }
      }

      .card-panel-icon {
        float: left;
        font-size: 48px;
      }

      .card-panel-description {
        float: right;
        margin: 26px;
        margin-right: 0;
        margin-left: 0;
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
