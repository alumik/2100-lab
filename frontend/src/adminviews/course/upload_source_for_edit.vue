<template>
  <div class="button-group">
    <b-button @click="showModal">
      管理资料
    </b-button>
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
        <b-row
          id="audio-row">
          <b-col cols="2"><h5>音频资料</h5></b-col>
          <b-col cols="8"><input
            v-model="audio_name"
            type="text"
            class="text-left audio-input"
          ></b-col>
          <b-col
            cols="2">
            <b-button @click="openAudioEntrance">打开</b-button>
          </b-col>
          <input
            id="upload-file"
            ref="input_audio"
            type="file"
            accept="audio/mp3"
            multiple="multiple"
            @change="handleAudioFileChange">
        </b-row>
        <b-row
          align-v="center">
          <b-col><h5 class="text-left">图片资料</h5></b-col>
        </b-row>
        <b-row class="my-row">
          <div
            v-if="has_origin_images"
            class="img-origin-preview-list">
            <div
              v-for="image in origin_image_copy_list"
              :key="image.image_id"
              class="img-uploader-preview">
              <div class="preview-img">
                <b-img
                  :src="image.image_path"
                  thumbnail
                  fluid
                  alt="Thumbnail"/>
              </div>
              <img
                src="../../assets/close.png"
                class="img-uploader-delete-btn"
                @click="deleteOriginImg(image.image_id)">
            </div>
          </div>
          <div
            ref="uploader"
            class="img-uploader"
            @drop="handlePicDrop">
            <p
              v-if="!hasImages"
              class="img-uploader-placeholder">{{ placeholder }}</p>
            <div
              v-if="hasImages"
              class="img-uploader-preview-list">
              <div
                v-for="(data,index) in imageDataList"
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
                  v-if="hasImages"
                  class="img-uploader-mask">
                  <p
                    class="img-uploader-file-name"
                    @click="openPicInput()">
                    {{ placeholder }}</p>
                </div>
                <img
                  src="../../assets/close.png"
                  class="img-uploader-delete-btn"
                  @click="deleteImg(index)">
              </div>
            </div>
            <label
              v-if="!hasImages"
              for="inputID"
              class="img-uploader-label"/>
            <input
              id="inputID"
              ref="input"
              class="input-image col-lg-12"
              type="file"
              accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
              multiple="multiple"
              @change="handlePicFileChange">
          </div>
        </b-row>
      </b-container>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <b-button
              @click="uploadResource">上传</b-button>
          </b-col>
          <b-col cols="2">
            <b-button
              @click="hideModal">取消</b-button>
          </b-col>
        </b-row>
      </div>
    </b-modal>
  </div>
</template>

<script>
import resizeImage from './resize'
export default {
  name: 'UploadSourceForEdit',
  props: {
    course_id: {
      type: String,
      default: '新增课程'
    },
    origin_image_list: {
      type: Array,
      default: () => {}
    },
    origin_audio_list: {
      type: Array,
      default: () => {}
    }
  },
  data () {
    return {
      audioFileList: [],
      audio_name: '',
      placeholder: '请选择上传文件',
      imageDataList: [],
      imageFileList: [],
      origin_image_copy_list: [],
      origin_delete_image_index: []
    }
  },
  computed: {
    hasImages () {
      return this.imageDataList.length > 0
    },
    has_origin_images () {
      return this.origin_image_copy_list.length > 0
    }
  },
  methods: {
    handleAudioFileChange () {
      let input = this.$refs.input_audio
      let files = input.files
      if (files && files.length === 1) {
        this.audioFileList.length = 0
        this.audioFileList.push(files[0])
        this.audio_name = files[0].name
      }
    },
    handlePicFileChange () {
      let input = this.$refs.input
      let files = input.files
      let _this = this
      if (!files || !window.FileReader) return

      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let reader = new FileReader()
        reader.onload = function (e) {
          resizeImage(e.target.result, 150, 150, function (result) {
            _this.imageDataList.push(result)
            _this.imageFileList.push(file)
          })
        }
        reader.readAsDataURL(file)
      }
    },
    handlePicDrop (e) {
      let files = e.dataTransfer.files
      this.preview(files)
    },
    openPicInput () {
      this.$refs.input.click()
    },
    deleteImg (index) {
      this.imageDataList.splice(index, 1)
      this.imageFileList.splice(index, 1)
    },
    deleteOriginImg (index) {
      let i = 0
      for (i = 0; i < this.origin_image_copy_list.length; i++) {
        if (this.origin_image_copy_list[i].image_id === index) {
          break
        }
      }
      this.origin_image_copy_list.splice(i, 1)
      this.origin_delete_image_index.push(index)
    },
    showModal () {
      this.origin_image_copy_list.length = 0
      if (this.origin_audio_list.length === 1) {
        this.audio_name = this.origin_audio_list[0]
      }
      if (this.origin_image_list.length > 0) {
        for (let i = 0; i < this.origin_image_list.length; i++) {
          this.origin_image_copy_list.push(this.origin_image_list[i])
        }
      }
      this.$refs.upload_source.show()
    },
    hideModal () {
      this.origin_delete_image_index.length = 0
      this.$refs.upload_source.hide()
    },
    openAudioEntrance () {
      this.$refs.input_audio.click()
    },
    uploadResource () {
      let uploadPicResourse = []
      for (let i = 1; i <= this.imageDataList.length; i++) {
        uploadPicResourse.push({
          'file': this.imageFileList[i - 1],
          'image': this.imageDataList[i - 1],
          'index': i,
          'time': ''
        })
      }
      this.$refs.upload_source.hide()
      this.$emit('uploadResource', uploadPicResourse, this.audioFileList, this.origin_delete_image_index)
    }
  }
}
</script>

<style scoped>
.button-group {
  display: flex;
  flex-direction: row;
  justify-content: left;
  max-width: 8rem;
}

.audio-input {
  width: 100%;
}

.define-btn {
  display: flex;
  flex-direction: row;
  justify-content: right;
}

.my-container {
  width: 100%;
  padding: 0;
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

.img-origin-preview-list {
  width: 95%;
  height: calc(150px + 18px * 2);
  margin-bottom: 10px;
  margin-left: 2.5%;
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
</style>
