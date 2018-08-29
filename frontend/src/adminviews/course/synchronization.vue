<template>
  <div>
    <Alert
      :count_down="wrong_count_down"
      :instruction="wrong"
      variant="danger"
      @decrease="wrong_count_down-1"
      @zero="wrong_count_down=0"/>
    <a
      id="sync-btn"
      class="btn"
      @click="show_modal">
      <simple-line-icons
        id="change-icon"
        icon="picture"
        color="white"
        class="icon"/>
      音图片同步
    </a>
    <b-modal
      ref="sync_picture"
      size="lg"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3>音图片同步</h3>
      </div>
      <div class="my-body">
        <b-container
          fluid
          class="choose-list">
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
              <a
                id="cut-btn"
                class="btn"
                @click="choose">
                截取时间
              </a>
            </b-col>
          </b-row>
        </b-container>
        <div class="table-data">
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
                  <a
                    id="delete-button"
                    class="btn"
                    @click="delete_some_data(data.index)">
                    删除</a>
                </td>
            </tr></tbody>
          </table>
        </div>
      </div>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <a
              id="upload-btn"
              class="btn"
              @click="upload_time_data">
              上传
            </a>
          </b-col>
          <b-col cols="2">
            <a
              id="cancel-btn"
              class="btn"
              @click="hide_modal">
              取消
            </a>
          </b-col>
        </b-row>
      </div>
    </b-modal>
  </div>
</template>

<script>
import Basic from '../basic/basic'
import PreSortPicture from './pre_sort_picture'
import Alert from '../../components/alert'

export default {
  name: 'SyncPicture',
  components: { Alert, PreSortPicture, Basic },
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
      now_number: 1,
      work_done: false,
      wrong_count_down: 0,
      wrong: '',
      dismiss_second: 5
    }
  },
  watch: {
    now_number (new_value, old_value) {
      this.attr[new_value] = 'primary'
      this.attr[old_value] = ''
      let temp = []
      for (let at of this.attr) {
        temp.push(at)
      }
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
      for (
        ;
        this.now_number <= this.image_data_list.length;
        this.now_number++
      ) {
        if (this.image_data_list[this.now_number - 1].time === '') {
          break
        }
      }
      if (this.audio_file_list.length === 1) {
        if (this.is_audio_changed === true) {
          this.audio_file_url = URL.createObjectURL(this.audio_file_list[0])
        } else {
          this.audio_file_url = this.audio_file_list[0]
        }
        this.$refs.sync_picture.show()
      } else {
        this.wrong = 'Upload Audio First'
        this.wrong_count_down = this.dismiss_second
      }
    },
    hide_modal () {
      this.$refs.sync_picture.hide()
      this.$refs.player.pause()
    },
    upload_time_data () {
      if (this.now_number - 1 === this.image_data_list.length) {
        this.$emit('sync_picture_audio', this.image_data_list)
        this.$refs.sync_picture.hide()
        this.$refs.player.pause()
      } else {
        this.wrong = 'WORK NOT FINISHED'
        this.wrong_count_down = this.dismiss_second
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

.my-body {
  margin-right: 16px;
  margin-left: 16px;
}

.choose-list {
  width: 100%;
  min-height: 270px;
  max-height: 270px;
  overflow: hidden;
  overflow-x: auto;
}

.card-picture {
  width: 90%;
  max-width: 200px;
  height: 240px;
  min-height: 240px;
  margin-top: 10px;
  overflow: hidden;
}

#cut-btn {
  margin-top: 5px;
}

#upload-btn,
#cancel-btn,
#cut-btn {
  color: white;
  background-color: #337ab7;
}

#upload-btn:hover,
#cancel-btn:hover,
#cut-btn:hover {
  background-color: #286090;
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
  height: 270px;
  overflow: hidden;
  overflow-x: auto;
  background-color: lightgray;
}

.table-data {
  height: 200px;
  overflow-y: scroll;
  text-align: center;
}

#delete-button {
  color: white;
  background-color: #dd514c;
}

#delete-button:hover,
#delete-button:active {
  background-color: #ba2d28;
}

#sync-btn {
  margin-right: 5px;
  margin-left: 5px;
  color: white;
  background-color: #337ab7;
}

#sync-btn:hover {
  background-color: #286090;
}
</style>
