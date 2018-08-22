<template>
  <Basic
    :items="items"
    class="special">
    <div class="my-content">
      <h2>音图片同步</h2>
      <PreSortPicture class="head-btn"/>
      <b-container
        fluid
        class="p-2 pre-scrollable choose-list">
        <b-card-group
          deck
          class="choose-row">
          <div
            v-for="img in imageDataList"
            :key="img.index"
            class="card-pic">
            <b-card
              :img-src="img.data"
              :title="img.index.toString()"
              :border-variant="attr[img.index]"
              img-alt="Image"
              img-bottom
              class="card-picture"
              @click="click(img)"/>
          </div>
        </b-card-group>
      </b-container>
      <b-container class="my-row">
        <b-row>
          <b-col
            cols="11">
            <audio
              ref="player"
              controls
              preload
              class="audio-player">
              <source
                src=""
                type="audio/mpeg">
              您的浏览器不支持 audio 元素。
            </audio>
          </b-col>
          <b-col
            class="cut-time"
            cols="1">
            <b-btn @click="choose">
              截取时间
            </b-btn>
          </b-col>
        </b-row>
      </b-container>
      <div class="table-data p-2 pre-scrollable">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">编号</th>
              <th scope="col">时间</th>
              <th scope="col">图片</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="data in choose_data"
              :key="data.id"
              align="center">
              <td>{{ data.index }}</td>
              <td>{{ data.time }}</td>
              <td>{{ data.name }}</td>
              <td>
                <button
                  type="button"
                  class="row inner-btn btn-sm"
                  @click="jump(admin.id)"
                >详情</button>
              </td>
          </tr></tbody>
        </table>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import PreSortPicture from './pre_sort_picture'
export default {
  name: 'SyncPicture',
  components: {PreSortPicture, Basic},
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        }, {
          text: '课程管理',
          href: '/admin/course'
        }, {
          text: this.$route.query.course_id,
          href: '/admin/course' + this.$route.query.url
        }, {
          text: '音图片同步',
          active: true
        }],
      attr: ['', 'primary'],
      now_number: 1,
      imageDataList: [
        {
          data: require('../../userviews/components/image/1.jpg'),
          index: 1
        }, {
          data: require('../../userviews/components/image/2.jpg'),
          index: 2
        }, {
          data: require('../../userviews/components/image/3.jpg'),
          index: 3
        }, {
          data: require('../../userviews/components/image/4.jpg'),
          index: 4
        }, {
          data: require('../../userviews/components/image/5.jpg'),
          index: 5
        }, {
          data: require('../../userviews/components/image/6.jpg'),
          index: 6
        }, {
          data: require('../../userviews/components/image/7.jpg'),
          index: 7
        }],
      choose_data: []
    }
  },
  watch: {
    now_number (newValue, oldValue) {
      this.attr[newValue] = 'primary'
      this.attr[oldValue] = ''
      let temp = []
      for (let at of this.attr) { temp.push(at) }
      this.attr = temp
    }
  },
  methods: {
    choose () {
      if (this.now_number < this.imageDataList.length) {
        this.choose_data.push({
          index: this.now_number,
          time: this.$refs.player.currentTime,
          name: (this.imageDataList[this.now_number - 1].index)
        })
        this.now_number += 1
      }
    },
    click (img) {
      this.now_number = img.index
    }
  }
}
</script>

<style scoped>
  .special {
    min-width: 1300px;
  }

  .my-content {
    margin: 40px;
    text-align: left;
  }

  .head-btn {
    display: inline-block;
    float: right;
  }

  .my-row {
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .audio-player {
    width: 100%;
  }

  .choose-list {
    width: 100%;
    min-height: 400px;
    max-height: 400px;
    margin-top: 50px;
  }

  .card-picture {
    width: 90%;
    min-width: 200px;
    height: 300px;
    min-height: 300px;
    overflow: hidden;
  }

  .card-pic {
    width: 100%;
    min-width: 250px;
    height: 100px;
    max-height: 100px;
  }

  .choose-row {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    min-width: 1000px;
    max-width: 1000px;
    height: 100px;
    max-height: 100px;
    margin-bottom: 50px;
  }

  .table-data {
    overflow: paged-y;
  }
</style>
