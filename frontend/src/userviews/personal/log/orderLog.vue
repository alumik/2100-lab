<template>
  <div id="page">
    <UserNavbar
      id="nav"
      @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
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
            :responsive="responsive"
            striped
            hover/>
          <b-pagination
            :total-rows="items.length"
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
  name: 'OrderLog',
  components: {
    UserNavbar,
    UserMenu,
    BreadCrumb
  },
  data: function () {
    return {
      hidden: false,
      list: [
        { id: 0, text: '查看学习记录', isActive: false },
        { id: 1, text: '查看订单记录', isActive: true }
      ],
      responsive: 'lg',
      fields: {
        order_no: {
          label: '订单号',
          sortable: true
        },
        course_codename: {
          label: '课程编号'
        },
        course_title: {
          key: 'age',
          label: '课程名',
          sortable: true
        },
        created_at: {
          key: '时间'
        },
        money: {
          label: '金额'
        }
      },
      crumbs: [
        {
          text: '个人中心',
          href: '/personal'
        },
        {
          text: '订单记录',
          href: '/personal/orderlog'
        }
      ],
      items: [],
      currentPage: 1,
      perPage: 10,
      page_nums: 1,
      pageOptions: [5, 10, 15]
    }
  },
  mounted () {
    let that = this
    axios
      .get(
        'http://localhost:8000/api/v1/customers/forestage/personal-center/get_order_logs/',
        {
          params: {
            page: that.currentPage,
            page_limit: that.perPage
          }
        }
      )
      .then(res => {
        that.page_nums = res.data.num_pages
        for (let data of res.data.content) {
          data.latest_learn = data.latest_learn
            .toString()
            .substring(0, 19)
            .replace('T', ' ')
          data.expire_time = data.expire_time.toString().substring(0, 19)
          that.items.push(data)
        }
      })
    setTimeout(() => {
      for (let i = 2; i <= that.page_nums; i = i + 1) {
        axios
          .get(
            'http://localhost:8000/api/v1/customers/forestage/personal-center/get-learning-logs/',
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
                data.created_at = data.created_at
                  .toString()
                  .substring(0, 19)
                  .replace('T', ' ')
                that.items.push(data)
              }
            }
          })
        if (i > that.page_nums) {
          break
        }
      }
    }, 1000)
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
}

.content {
  padding: 20px;
}

.my-0 {
  justify-content: center;
}
</style>
