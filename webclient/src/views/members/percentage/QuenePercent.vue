<template>
  <div>
    <el-progress
      type="dashboard"
      :percentage="percentage"
      :color="colors"
    ></el-progress>
    <el-button-group>
      <el-button icon="el-icon-minus" @click="decrease"></el-button>
      <el-button icon="el-icon-plus" @click="increase"></el-button>
    </el-button-group>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  percentage: number = 10;
  colors: [
    { color: "#f56c6c"; percentage: 20 },
    { color: "#e6a23c"; percentage: 40 },
    { color: "#5cb87a"; percentage: 60 },
    { color: "#1989fa"; percentage: 80 },
    { color: "#6f7ad3"; percentage: 100 }
  ];
  mounted() {}
  increase(): void {
    let myself = this;
    this.percentage += 10;
    if (this.percentage > 100) {
      myself.percentage = 100;
    }
  }
  decrease(): void {
    let myself = this;
    this.percentage -= 10;
    if (this.percentage < 0) {
      myself.percentage = 0;
    }
  }
  get computedTest() {
    return null;
  }
}
</script>
<style scoped></style>
