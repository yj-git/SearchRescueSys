<template>
  <div class="job-progress">
    <div class="title">
      <h3>{{ username }}</h3>
      <span>{{ casename }}</span>
      <span>{{ cmt | fortmatDate }}</span>
    </div>
    <el-progress :percentage="percent"></el-progress>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import moment from "moment";
@Component({
  filters: {
    fortmatDate(now: Date) {
      return moment(now).format("YYYY-MM-DD HH");
    }
  }
})
export default class center_map extends Vue {
  mydata: any = null;
  @Prop(Number)
  percent: number;
  @Prop(String)
  username: string;
  @Prop(String)
  casename: string;
  @Prop(Date)
  cmt: Date;
  mounted() {}
  get computedTest() {
    return null;
  }
  get date2Str(): string {
    return "null";
  }
}
</script>
<style scoped lang="less">
.job-progress {
  display: flex;
  align-items: baseline;
  .title {
    color: black;
    display: flex;
    flex: 2;
    h3 {
      display: flex;
      flex: 1;
      // flex: ;
    }
    span {
      display: flex;
      flex: 1;
    }
  }
  .el-progress {
    margin: 1em;
    display: flex;
    flex: 1;
  }
}
</style>
