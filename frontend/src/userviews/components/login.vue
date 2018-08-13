<template>
  <b-container fluid>
    <b-input-group prepend="手机号">
      <b-form-input type="number"/>
    </b-input-group>
  </b-container>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style scoped>
  b-container, b-input-group, b-form-input {
    display: block;
    width: 50px;
    max-width: 330px;
    margin: 0 auto;
  }
</style>
