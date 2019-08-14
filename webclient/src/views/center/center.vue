<template>
  <div id="center">
      <LeftBar></LeftBar>
      <router-view></router-view>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import LeftBar from "@/views/members/bar/leltBar.vue"
@Component({components:{
    LeftBar
}})
export default class center_map extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#center {
  display: flex;
  flex: 8;
  background: #80c3c5;
}
</style>