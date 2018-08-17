<template>
  <div>
    <b-btn @click="showModal">
      OPEN
    </b-btn>
    <b-modal
      ref="edit_picture"
      size="lg"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3 class="float-left">图片预排序</h3>
      </div>
      <b-container
        fluid
        class="p-4 bg-danger row pre-scrollable choose-list">
        <b-row
          v-for="img in sortImageDataList"
          :key="img.index"
          class="choose-row">
          <b-col>
            <b-img
              :src="img.data"
              fluid
              alt="test-image"
              class="img-thumbnail"
              @click="dropback(img)"/>
          </b-col>
        </b-row>
      </b-container>
      <b-container
        fluid
        class="p-4 bg-primary row pre-scrollable choose-list">
        <b-row
          v-for="img in chooseImageDataList"
          :key="img.data"
          class="choose-row"
        >
          <b-col>
            <b-img
              :src="img.data"
              fluid
              alt="test-image"
              class="img-thumbnail"
              @click="dropout(img)"/></b-col>
        </b-row>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'SortPicture',
  data () {
    return {
      chooseImageDataList: [
        {
          data: require('../../userviews/components/image/1.jpg'),
          index: 1
        },
        {
          data: require('../../userviews/components/image/2.jpg'),
          index: 2
        },
        {
          data: require('../../userviews/components/image/3.jpg'),
          index: 3
        },
        {
          data: require('../../userviews/components/image/4.jpg'),
          index: 4
        },
        {
          data: require('../../userviews/components/image/5.jpg'),
          index: 5
        },
        {
          data: require('../../userviews/components/image/6.jpg'),
          index: 6
        },
        {
          data: require('../../userviews/components/image/7.jpg'),
          index: 7
        }
      ],
      sortImageDataList: [],
      now_index: 0
    }
  },
  methods: {
    showModal () {
      this.$refs.edit_picture.show()
    },
    dropout (img) {
      let index = img.index
      for (let i = index; i < this.chooseImageDataList.length; i++) {
        this.chooseImageDataList[i].index -= 1
      }
      this.chooseImageDataList.splice(img.index - 1, 1)
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
      img.index = this.chooseImageDataList.length + 1
      this.chooseImageDataList.push(img)
    }
  }
}
</script>

<style scoped>
  .choose-list {
    display: flex;
    flex-direction: row;
    min-height: 200px;
    max-height: 200px;
  }

  .choose-row {
    width: 200px;
    max-width: 200px;
    height: 200px;
    max-height: 200px;
    padding: 5px;
  }
</style>
