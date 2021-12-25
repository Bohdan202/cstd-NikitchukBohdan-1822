<template>
  <div class="wrapper_loading">
    <img src="..\assets\gif\loading\3.gif" alt="Download" width=250/>
  </div>
</template>

<script>
export default {
  name: 'Loader'
}
</script>

<style lang="scss" scoped>

.wrapper_loading {
  display: table-cell;
  height: 90vh;
  text-align: center;
  width: 100vw;
  vertical-align: middle;
}

</style>