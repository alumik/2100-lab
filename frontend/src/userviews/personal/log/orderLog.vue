<template>
  <div id="page">
    <UserNavbar/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <div id="info">
        <BreadCrumb :items="crumbs"/>
        <b-table
          :items="items"
          :fields="fields"
          :current-page="currentPage"
          :per-page="perPage"
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
</template>

<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
import BreadCrumb from '../../../components/breadCrumb'
const Items = [
  {
    isActive: true,
    age: 40,
    first_name: 'Dickerson',
    last_name: 'Macdonald',
    address: { country: 'USA', city: 'New York' }
  },
  {
    isActive: false,
    age: 21,
    first_name: 'Larsen',
    last_name: 'Shaw',
    address: { country: 'Canada', city: 'Toronto' }
  },
  {
    isActive: false,
    age: 89,
    first_name: 'Geneva',
    last_name: 'Wilson',
    address: { country: 'Australia', city: 'Sydney' }
  },
  {
    isActive: true,
    age: 38,
    first_name: 'Jami',
    last_name: 'Carney',
    address: { country: 'England', city: 'London' }
  }
]
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
      fields: {
        last_name: {
          label: 'Person last name',
          sortable: true
        },
        first_name: {
          label: 'Person first name'
        },
        foo: {
          key: 'age',
          label: 'Person age',
          sortable: true
        },
        city: {
          key: 'address.city'
        },
        'address.country': {
          label: 'Country'
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
      items: Items.concat(Items.concat(Items.concat(Items.concat(Items)))),
      currentPage: 1,
      perPage: 10,
      pageOptions: [ 5, 10, 15 ]
    }
  },
  methods: {
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
    margin: 40px 20px;
  }
  .breadcrumb {
    margin-top: -40px;
    margin-left: -20px;
  }

  .my-0 {
    justify-content: center;
  }
</style>
