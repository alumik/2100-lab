<template>
  <div id="page">
    <UserNavbar
      id="nav"
      @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"
        class="menu"/>
      <div id="info">
        <BreadCrumb
          id="breadcrumb"
          :items="crumbs"/>
        <div class="content">
          <b-table
            :items="items"
            :fields="fields"
            :current-page="currentPage"
            :per-page="perPage"
            striped
            hover/>
          <b-pagination
            :total-rows="count"
            :per-page="perPage"
            v-model="currentPage"
            class="my-0" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
import BreadCrumb from '../../../components/breadCrumb'
import axios from 'axios'

export default {
  name: 'StudyLog',
  components: {
    UserNavbar,
    UserMenu,
    BreadCrumb
  },
  data: function () {
    return {
      hidden: false,
      list: [
        { id: 0, text: '查看学习记录', isActive: true },
        { id: 1, text: '查看订单记录', isActive: false }
      ],
      fields: {
        course_codename: {
          label: '课程代号'
        },
        course_title: {
          label: '课程名'
        },
        latest_learn: {
          label: '学习时间'
        },
        expire_time: {
          label: '过期时间'
        }
      },
      crumbs: [
        {
          text: '个人中心',
          href: '/personal'
        },
        {
          text: '学习记录',
          href: '/personal/studylog'
        }
      ],
      items: [],
      count: 0,
      currentPage: 1,
      perPage: 10,
      page_nums: 1,
      pageOptions: [5, 10, 15]
    }
  },
  async mounted () {
    let that = this
    let res = await axios.get(
      'http://localhost/api/v1/customers/forestage/personal-center/get-learning-logs/',
      {
        params: {
          page: that.currentPage,
          page_limit: that.perPage
        }
      }
    )
    that.count = res.data.count
    that.page_nums = res.data.num_pages
    for (let data of res.data.content) {
      data.latest_learn = data.latest_learn
        .toString()
        .substring(0, 19)
        .replace('T', ' ')
      data.expire_time = data.expire_time
        .toString()
        .substring(0, 19)
        .replace('T', ' ')
      that.items.push(data)
    }
    for (let i = 2; i <= that.page_nums; i++) {
      axios
        .get(
          'http://localhost/api/v1/customers/forestage/personal-center/get-learning-logs/',
          {
            params: {
              page: i,
              page_limit: that.perPage
            }
          }
        )
        .then(res => {
          that.page_nums = res.data.num_pages
          if (i <= res.data.num_pages) {
            for (let data of res.data.content) {
              data.latest_learn = data.latest_learn
                .toString()
                .substring(0, 19)
                .replace('T', ' ')
              data.expire_time = data.expire_time
                .toString()
                .substring(0, 19)
                .replace('T', ' ')
              that.items.push(data)
            }
          }
        })
    }
  },
  methods: {
    hide: function () {
      this.hidden = !this.hidden
    }
  }
}
</script>

<style scoped>
#page {
  height: 100%;
}

#main {
  display: flex;
  height: 100%;
}

#info {
  flex-grow: 1;
  overflow-x: auto;
}

.content {
  padding: 20px;
}

.my-0 {
  justify-content: center;
}
</style>
