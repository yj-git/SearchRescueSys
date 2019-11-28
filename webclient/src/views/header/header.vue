<template>
  <div id="header">
    <div class="logo"><img src="../../assets//nmefclog.png" /></div>
    <div class="title">
      <h2>国家海洋环境预报中心</h2>
      <h4>搜救溢油系统</h4>
    </div>
  </div>
</template>
<script lang="ts">
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
<style scoped lang="less">
#header {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  flex: 0.5;
  // background: #31859be8;
  background: linear-gradient(#465581, #313b59);
  .logo {
    position: absolute;
    left: 50px;
    img {
      height: 60px;
    }
  }
  .title {
    display: flex;
    flex-direction: row;
    // justify-content: center;
    align-content: baseline;
    h2 {
      line-height: 1.8;
      font-family: Arial, Helvetica, sans-serif;
      text-shadow: 2px 2px 10px #000;
      margin-right: 20px;
    }
    h4 {
      line-height: 1.8;
      font-family: Arial, Helvetica, sans-serif;
      text-shadow: 2px 2px 10px #000;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
  }
  /* background: url('../../assets/header_2.jpg'); */
}
</style>
