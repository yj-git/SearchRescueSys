<template>
  <div>
    <div id="time_bar">
      <div class="timebar container">
        <input class="form-control col-md-3" aria-describedby="emailHelp" v-model="current" />
        <button type="button" class="btn btn-primary" @click="setCurrentDate()">搜索</button>
      </div>
    </div>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class TimeBar extends Vue {
  mydata: any = null;
  current: String = "1990-01-01T6:00:00.0Z";
  // 修改当前的current的值
  setCurrentDate() {
    // console.log(val);
    // console.log(this.current);
    var tempCurrent = this.current;
    this.$store.commit("current", tempCurrent);
  }
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#time_bar {
  display: flex;
  flex: 10;
  background: rgba(210, 219, 77, 0.829);
  height: 50px;
}
.timebar {
  /* 横向排列即可 */
  display: flex;
}
</style>