<template>
  <body>
    <el-row
      :gutter="40"
      class="panel-group list-title">
      <div>付费课程推荐</div>
      <a
        class="watch-more"
        href="#">查看更多</a>
    </el-row>
    <el-row
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
              src="./image/9.jpg"
              class="card-panel-icon"
            >
          </div>
          <div class="card-panel-description">
            <div class="card-title card-panel-text">
              <div>physics</div>
              <a
                class="pay-style"
                href="#">购买课程</a>
            </div>
            <div class="card-panel-course-description">
              我与父亲不相见已二年余了，我最不能忘记的是他的背影。
            </div>
          </div>
        </div>
      </el-col>
      <el-col
        :xs="12"
        :sm="12"
        :lg="6"
        class="card-panel-col">
        <div
          class="card-panel"
          @click="handleSetLineChartData('cheeks')">
          <div class="card-panel-icon-wrapper icon-cheek">
            <img
              src="./image/2.jpg"
              class="card-panel-icon"
            >
          </div>
          <div class="card-panel-description card-panel-text">
            <div class="card-title card-panel-text">
              <div>chemistry</div>
              <a
                class="pay-style"
                href="#">购买课程</a>
            </div>
            <div class="card-panel-course-description">
              到徐州见着父亲，看见满院狼藉的东西，又想起祖母，不禁簌簌地流下眼泪。
            </div>
          </div>
        </div>
      </el-col>
      <el-col
        :xs="12"
        :sm="12"
        :lg="6"
        class="card-panel-col">
        <div
          class="card-panel"
          @click="handleSetLineChartData('seas')">
          <div class="card-panel-icon-wrapper icon-sea">
            <img
              src="./image/5.jpg"
              class="card-panel-icon"
            >
          </div>
          <div class="card-panel-description card-panel-text">
            <div class="card-title card-panel-text">
              <div>farmland</div>
              <a
                class="pay-style"
                href="#">购买课程</a>
            </div>
            <div class="card-panel-course-description">
              我看那边月台的栅栏外有几个卖东西的等着顾客。
              走到那边月台，须穿过铁道，须跳下去又爬上去。
            </div>
          </div>
        </div>
      </el-col>
      <el-col
        :xs="12"
        :sm="12"
        :lg="6"
        class="card-panel-col">
        <div
          class="card-panel"
          @click="handleSetLineChartData('oranges')">
          <div class="card-panel-icon-wrapper icon-orange">
            <img
              src="./image/3.jpg"
              class="card-panel-icon"
            >
          </div>
          <div class="card-panel-description card-panel-text ">
            <div class="card-title card-panel-text">
              <div>biology</div>
              <a
                class="pay-style"
                href="#">购买课程</a>
            </div>
            <div class="card-panel-course-description">
              我看见他戴着黑布小帽，穿着黑布大马褂，
              深青布棉袍，蹒跚地走到铁道边，慢慢探身下去，尚不大难。
            </div>
          </div>
        </div>
      </el-col>
      <el-col
        :xs="12"
        :sm="12"
        :lg="6"
        class="card-panel-col">
        <div
          class="card-panel"
          @click="handleSetLineChartData('apples')">
          <div class="card-panel-icon-wrapper icon-apple">
            <img
              src="./image/4.jpg"
              class="card-panel-icon"
            >
          </div>
          <div class="card-panel-description card-panel-text">
            <div class="card-title card-panel-text">
              <div>navigate</div>
              <a
                class="pay-style"
                href="#">购买课程</a>
            </div>
            <div class="card-panel-course-description">
              近几年来，父亲和我都是东奔西走，家中光景是一日不如一日。
              他少年出外谋生，独力支持，做了许多大事。
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </body>
</template>

<script>
export default {
  name: 'PaidRecommendList',
  methods: {
    handleSetLineChartData (type) {
      this.$emit('handleSetLineChartData', type)
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

      .card-title {
        display: flex;
        flex-direction: row;
      }

      .pay-style {
        margin-left: 10px;
        color: #777;

        &.hover {
          color: #8a2be2;
          text-decoration: none;
        }
      }

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
