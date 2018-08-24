<template>
  <div>
    <b-btn
      class="head-btn"
      @click="showModal">
      图片预排序
    </b-btn>
    <b-modal
      ref="edit_picture"
      size="lg"
      ok-title="确认"
      cancel-title="取消"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3 class="float-left">图片预排序</h3>
      </div>
      <b-container
        fluid
        class="bg-danger row pre-scrollable choose-list">
        <b-row
          v-for="img in sortImageDataList"
          :key="img.index"
          class="choose-row">
          <b-col>
            <b-img
              :src="img.image"
              fluid
              alt="test-image"
              class="img-thumbnail"
              @click="dropback(img)"/>
          </b-col>
        </b-row>
      </b-container>
      <b-container
        fluid
        class="bg-primary row pre-scrollable choose-list">
        <b-row
          v-for="img in choose_image_data_list"
          :key="img.data"
          class="choose-row"
        >
          <b-col>
            <b-img
              :src="img.image"
              fluid
              alt="test-image"
              class="img-thumbnail"
              @click="dropout(img)"/>
          </b-col>
        </b-row>
      </b-container>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <b-button
              @click="sendModal">上传</b-button>
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
export default {
  name: 'PreSortPicture',
  props: {
    choose_image_data_list_origin: {
      default: () => {},
      type: Array
    }
  },
  data: function () {
    return {
      sortImageDataList: [],
      choose_image_data_list: [],
      now_index: 0
    }
  },
  methods: {
    showModal () {
      this.now_index = 0
      this.choose_image_data_list = []
      this.sortImageDataList = []
      this.choose_image_data_list.length = 0
      for (let i = 0; i < this.choose_image_data_list_origin.length; i++) {
        this.choose_image_data_list.push(this.choose_image_data_list_origin[i])
      }
      this.$refs.edit_picture.show()
    },
    dropout (img) {
      let index = img.index
      for (let i = index; i < this.choose_image_data_list.length; i++) {
        this.choose_image_data_list[i].index -= 1
      }
      this.choose_image_data_list.splice(img.index - 1, 1)
      img.index = this.now_index + 1
      this.now_index += 1
      this.sortImageDataList.push(img)
    },
    dropback (img) {
      this.now_index -= 1
      for (let i = img.index; i < this.sortImageDataList.length; i++) {
        this.sortImageDataList[i].index -= 1
      }
      this.sortImageDataList.splice(img.index - 1, 1)
      img.index = this.choose_image_data_list.length + 1
      this.choose_image_data_list.push(img)
    },
    sendModal () {
      this.now_index = 0
      this.$emit('uploadSortedPic', this.sortImageDataList.slice())
      this.choose_image_data_list.length = 0
      this.choose_image_data_list_origin.length = 0
      this.sortImageDataList.length = 0
      this.$refs.edit_picture.hide()
    },
    hideModal () {
      this.now_index = 0
      this.$emit('uploadSortedPic', this.choose_image_data_list_origin.slice())
      this.choose_image_data_list.length = 0
      this.choose_image_data_list_origin.length = 0
      this.sortImageDataList.length = 0
      this.$refs.edit_picture.hide()
    }
  }
}
</script>

<style scoped>
  .head-btn {
    display: inline-block;
    float: right;
  }

  .choose-list {
    display: flex;
    flex-direction: row;
    min-height: 200px;
    max-height: 200px;
    padding: 0;
    margin: 0
  }

  .choose-row {
    width: 200px;
    max-width: 200px;
    height: 200px;
    max-height: 200px;
    padding: 5px;
  }
</style>
