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
            :current-page="current_page"
            :per-page="per_page"
            :responsive="responsive"
            striped
            hover/>
          <b-pagination
            :total-rows="count"
            :per-page="per_page"
            v-model="current_page"
            class="my-0" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
import BreadCrumb from '../../../components/bread_crumb'
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
          label: '订单号'
        },
        course_codename: {
          label: '课程编号'
        },
        course_title: {
          label: '课程名'
        },
        created_at: {
          label: '创建时间'
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
      count: 0,
      current_page: 1,
      per_page: 10,
      page_nums: 1,
      pageOptions: [5, 10, 15]
    }
  },
  async mounted () {
    let that = this
    let res = await axios.get(
      'http://localhost/api/v1/customers/forestage/personal-center/get-order-logs/',
      {
        params: {
          page: that.current_page,
          page_limit: that.per_page
        }
      }
    )
    that.count = res.data.count
    that.page_nums = res.data.num_pages
    for (let data of res.data.content) {
      data.created_at = data.created_at
        .toString()
        .substring(0, 19)
        .replace('T', ' ')
      that.items.push(data)
    }
    for (let i = 2; i <= that.page_nums; i++) {
      axios
        .get(
          'http://localhost/api/v1/customers/forestage/personal-center/get-order-logs/',
          {
            params: {
              page: i,
              page_limit: that.per_page
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
  margin-top: 60px;
}

.my-0 {
  justify-content: center;
}

#breadcrumb {
  display: none;
  padding: 20px;
}

@media (max-width: 768px) {
  #breadcrumb {
    display: flex;
  }

  .content {
    margin-top: 0;
  }
}
</style>
