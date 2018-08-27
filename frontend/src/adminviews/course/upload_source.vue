<template>
  <div>
    <a
      id="manage-btn"
      class="btn"
      @click="show_modal">
      <simple-line-icons
        id="change-icon"
        icon="picture"
        color="white"
        class="icon"/>
      管理资料
    </a>
    <b-modal
      ref="upload_source"
      size="lg"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3 class="float-left">上传课程资料</h3>
      </div>
      <b-container class="my-container">
        <b-row>
          <b-col cols="2"><h5>音频资料</h5></b-col>
          <b-col cols="8"><input
            v-model="audio_name"
            type="text"
            class="text-left form-control audio-input"
          ></b-col>
          <b-col
            cols="2">
            <a
              id="open-upload-btn"
              class="btn"
              @click="open_audio_entrance">
              上传
            </a>
          </b-col>
          <input
            id="upload-file"
            ref="input_audio"
            type="file"
            accept="audio/mp3"
            multiple="multiple"
            @change="handle_audio_file_change">
        </b-row>
        <b-row
          align-v="center">
          <b-col><h5 class="text-left">图片资料</h5></b-col>
        </b-row>
        <b-row class="my-row">
          <div
            ref="uploader"
            class="img-uploader"
            @drop="handle_pic_drop">
            <p
              v-if="!has_images"
              class="img-uploader-placeholder">{{ placeholder }}</p>
            <div
              v-if="has_images"
              class="img-uploader-preview-list">
              <div
                v-for="(data,index) in image_data_list"
                :key="index"
                class="img-uploader-preview">
                <div class="preview-img">
                  <b-img
                    :src="data"
                    thumbnail
                    fluid
                    alt="Thumbnail"/>
                </div>
                <div
                  v-if="has_images"
                  class="img-uploader-mask">
                  <p
                    class="img-uploader-file-name"
                    @click="open_pic_input()">
                    {{ placeholder }}</p>
                </div>
                <img
                  src="../../assets/close.png"
                  class="img-uploader-delete-btn"
                  @click="delete_img(index)">
              </div>
            </div>
            <label
              v-if="!has_images"
              for="inputID"
              class="img-uploader-label"/>
            <input
              id="inputID"
              ref="input"
              class="input-image col-lg-12"
              type="file"
              accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
              multiple="multiple"
              @change="handle_picture_file_change">
          </div>
        </b-row>
      </b-container>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <a
              id="upload-btn"
              class="btn"
              @click="upload_resource">
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
import resize_image from './resize'
export default {
  name: 'UploadSource',
  props: {
    course_id: {
      type: String,
      default: '新增课程'
    }
  },
  data () {
    return {
      audio_file_list: [],
      audio_name: '',
      placeholder: '请选择上传文件',
      origin_image_list: [],
      image_data_list: [],
      image_file_list: []
    }
  },
  computed: {
    has_images () {
      return this.image_data_list.length > 0
    }
  },
  methods: {
    handle_audio_file_change () {
      let input = this.$refs.input_audio
      let files = input.files
      if (files && files.length === 1) {
        this.audio_file_list.length = 0
        this.audio_file_list.push(files[0])
        this.audio_name = files[0].name
      }
    },
    handle_picture_file_change () {
      let input = this.$refs.input
      let files = input.files
      let _this = this
      if (!files || !window.FileReader) {
        return
      }
      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let reader = new FileReader()
        reader.onload = function (e) {
          resize_image(e.target.result, 150, 150, function (result) {
            _this.image_data_list.push(result)
            _this.image_file_list.push(file)
          })
        }
        reader.readAsDataURL(file)
      }
    },
    handle_pic_drop (e) {
      let files = e.dataTransfer.files
      this.preview(files)
    },
    open_pic_input () {
      this.$refs.input.click()
    },
    delete_img (index) {
      this.image_data_list.splice(index, 1)
      this.image_file_list.splice(index, 1)
    },
    show_modal () {
      this.$refs.upload_source.show()
    },
    hide_modal () {
      this.$refs.upload_source.hide()
    },
    open_audio_entrance () {
      this.$refs.input_audio.click()
    },
    upload_resource () {
      let upload_picture_resourse = []
      for (let i = 1; i <= this.image_data_list.length; i++) {
        upload_picture_resourse.push({
          file: this.image_file_list[i - 1],
          image: this.image_data_list[i - 1],
          index: i,
          time: ''
        })
      }
      this.$refs.upload_source.hide()
      this.$emit(
        'upload_resource',
        upload_picture_resourse,
        this.audio_file_list
      )
    }
  }
}
</script>

<style scoped>
h5 {
  margin-top: 20px;
  margin-bottom: 20px;
}

#open-upload-btn {
  margin-top: 20px;
  margin-left: 10px;
}

#upload-btn,
#cancel-btn,
#open-upload-btn {
  color: white;
  background-color: #337ab7;
}

#upload-btn:hover,
#cancel-btn:hover,
#open-upload-btn:hover {
  background-color: #286090;
}

.audio-input {
  width: 100%;
  margin-top: 20px;
}

.define-btn {
  display: flex;
  flex-direction: row;
  justify-content: right;
}

.my-container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin: 0;
}

#upload-file {
  display: none;
}

.input-image {
  display: none;
}

.img-uploader {
  position: relative;
  width: 100%;
  min-width: 260px;
  max-width: 800px;
  height: calc(150px + 25px * 2);
  margin-right: 2%;
  margin-left: 2%;
  background: #ebebeb;
  border-radius: 5px;
}

.img-uploader-placeholder {
  position: absolute;
  top: 50%;
  width: 100%;
  margin: 0;
  font-size: 15px;
  color: #aaa;
  text-align: center;
  transform: translate(0%, -50%);
}

.img-uploader-preview-list {
  width: 100%;
  height: calc(150px + 18px * 2);
  overflow: hidden;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-backface-visibility: hidden;
  -webkit-overflow-scrolling: touch;
}

.img-uploader-preview {
  z-index: 2;
  display: inline-block;
  min-height: 150px;
  margin: 10px;
  background: #333;
  border-radius: 10px;
  transition: 0.3s cubic-bezier(0.3, 0, 0.2, 1);
}

.img-uploader-mask {
  position: absolute;
  bottom: 0;
  display: none;
  width: 150px;
  text-align: center;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 1px;
}

.img-uploader-preview:hover {
  transform: scale(1.02);
}

.img-uploader-preview:hover .img-uploader-mask {
  display: block;
}

.img-uploader-delete-btn {
  position: absolute;
  top: 0;
  right: 0;
  display: none;
  width: 25px;
  height: 25px;
  margin: 5px;
}

.img-uploader-preview:hover .img-uploader-delete-btn {
  display: block;
}

.img-uploader-preview .preview-img {
  width: 150px;
  height: 150px;
  overflow: hidden;
}

.img-uploader-label {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  margin-bottom: 0;
  cursor: pointer;
}

.img-uploader-file-name {
  display: inline-block;
  max-width: 90%;
  padding-top: 10px;
  margin: 0;
  overflow: hidden;
  font-size: 5px;
  color: white;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

#manage-btn {
  margin-right: 5px;
  margin-left: 5px;
  color: white;
  background-color: #337ab7;
}

#manage-btn:hover {
  background-color: #286090;
}
</style>
