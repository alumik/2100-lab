<template>
  <div>
    <UserNavbar/>
    <div id="main">
      <UserMenu
        :list="list"/>
      <b-table
        :items="items"
        :fields="fields"
        striped
        hover/>
    </div>
  </div>
</template>
<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
export default {
  name: 'StudyLog',
  components: {
    UserNavbar,
    UserMenu
  },
  data: function () {
    return {
      list: [
        {id: 0, text: '查看学习记录', isActive: true},
        {id: 1, text: '查看订单记录', isActive: false}
      ],
      fields: {
        last_name: {
          label: 'Person last name',
          sortable: true
        },
        first_name: {
          label: 'Person first name',
          sortable: false
        },
        foo: {
          // This key overrides `foo`!
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
      items: [
        { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald', address: { country: 'USA', city: 'New York' } },
        { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw', address: { country: 'Canada', city: 'Toronto' } },
        { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson', address: { country: 'Australia', city: 'Sydney' } },
        { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney', address: { country: 'England', city: 'London' } }
      ]
    }
  },
  methods: {
  }
}
</script>

<style scoped>
  img {
    width: 40px;
    height: 40px;
  }
  div {
    height: 100%;
  }
  #main {
    display: flex;
    height: 100%;
  }
</style>
