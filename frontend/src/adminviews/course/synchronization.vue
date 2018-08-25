<template>
  <div>
    <b-button @click="show_modal">
      音图片同步
    </b-button>
    <b-modal
      ref="sync_picture"
      size="lg"
      centered
      no-close-on-esc>
      <h2>音图片同步</h2>
      <b-container
        fluid
        class="p-2 pre-scrollable choose-list">
        <b-card-group
          deck
          class="choose-row">
          <div
            v-for="img in image_data_list"
            :key="img.id"
            class="card-pic">
            <b-card
              :img-src="img.image"
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
            cols="10">
            <audio
              ref="player"
              :src="audio_file_url"
              controls
              preload
              type="audio/mp3"
              class="audio-player">
              您的浏览器不支持 audio 元素。
            </audio>
          </b-col>
          <b-col
            class="cut-time"
            cols="2">
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
              v-for="data in image_data_list"
              :key="data.id"
              align="center">
              <td>{{ data.index }}</td>
              <td>{{ data.time }}</td>
              <td>{{ data.name }}</td>
              <td>
                <button
                  type="button"
                  class="row inner-btn btn-sm"
                  @click="delete_some_data(data.index)"
                >删除</button>
              </td>
          </tr></tbody>
        </table>
      </div>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <b-button
              @click="upload_time_data">上传</b-button>
          </b-col>
          <b-col cols="2">
            <b-button
              @click="hide_modal">取消</b-button>
          </b-col>
        </b-row>
      </div>
    </b-modal>
  </div>
</template>

<script>
import Basic from '../basic/basic'
import PreSortPicture from './pre_sort_picture'
export default {
  name: 'SyncPicture',
  components: {PreSortPicture, Basic},
  props: {
    image_data_list: {
      default: () => {},
      type: Array
    },
    audio_file_list: {
      default: () => {},
      type: Array
    },
    is_audio_changed: {
      default: false,
      type: Boolean
    }
  },
  data () {
    return {
      audio_file_url: '',
      attr: ['', 'primary'],
      now_number: 1
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
      if (this.now_number === 1) {
        this.$refs.player.play()
      }
      if (this.now_number <= this.image_data_list.length) {
        this.image_data_list[this.now_number - 1].time = this.$refs.player.currentTime
        this.now_number += 1
      }
    },
    click (img) {
      this.now_number = img.index
    },
    delete_some_data (index) {
      if (this.image_data_list[index - 1]) {
        this.image_data_list[index - 1].time = ''
        this.now_number = index
      }
    },
    show_modal () {
      if (this.audio_file_list.length === 1) {
        if (this.is_audio_changed === true) {
          this.audio_file_url = URL.createObjectURL(this.audio_file_list[0])
        } else {
          this.audio_file_url = this.audio_file_list[0]
        }
        this.$refs.sync_picture.show()
      } else {
        alert('Upload Audio First')
      }
    },
    hide_modal () {
      this.$refs.sync_picture.hide()
    },
    upload_time_data () {
      console.log(this.now_number)
      if (this.now_number - 1 === this.image_data_list.length) {
        this.$emit('sync_picture_audio', this.image_data_list)
      } else {
        alert('WORK NOT FINISHED')
      }
    }
  }
}
</script>

<style scoped>
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
