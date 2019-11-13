<template>
  <div id="right_bar"></div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class RightOilBar extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#right_bar {
  background: red;
  /* height: 500px; */
  position: absolute;
  top: 50px;
  right: 50px;
  height: 500px;
  width: 200px;
  padding: 10px;
}
</style>