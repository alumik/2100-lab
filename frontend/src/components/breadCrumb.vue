<template>
  <b-breadcrumb :items="items"/>
</template>

<script>
export default {
  name: 'BreadCrumb',
  props: {
    items: {
      type: Array,
      default: null
    }
  }
}
</script>
