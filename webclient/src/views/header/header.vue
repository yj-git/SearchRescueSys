<template>
  <div id="header">header</div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class header extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#header {
  display: flex;
  flex-direction: column;
  /* flex: 1; */
  background: #2c3e50;
}
</style>