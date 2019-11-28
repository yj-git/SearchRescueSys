<template>
  <div class="data-box">
    <div class="box-title">
      <h4>{{title}}</h4>
    </div>
    <div class="box-body">
      <div class="box-row" v-bind:key="item.key" v-for="item in modelData">
        <h4>{{item.title}}</h4>
        <span>{{item.val}}</span>
      </div>
    </div>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class DataBox extends Vue {
  mydata: any = null;
  //   modelData: { title: string; val: string }[] = [
  //     {
  //       title: "测试1",
  //       val: "5.6"
  //     },
  //     {
  //       title: "测试2",
  //       val: "322"
  //     },
  //     {
  //       title: "测试3",
  //       val: "海浪"
  //     }
  //   ];
  @Prop(Array)
  modelData: { title: string; val: string }[];
  @Prop(String)
  title: string;
  mounted() {
    // this.modelData = [];
  }
  get computedTest() {
    return null;
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base";
.data-box {
  @allradius();
  @formmoreshadow();
  display: flex;
  flex: 1;
  flex-direction: column;
  //   background: rgb(204, 166, 60);
  background: linear-gradient(40deg, #283958 30%, #151e52);
  height: 180px;
  margin: 1em;
  .box-title {
    display: flex;
    font-size: 1.1rem;
    font-weight: 500;
    color: white;
    justify-content: flex-start;
    padding-left: 1.5em;
    padding-top: 0.75em;
    @divshadow();
  }
  .box-body {
    display: flex;
    flex-direction: column;
    padding-bottom: 0.5em;
    .box-row {
      padding-top: 0.25em;
      display: flex;
      justify-content: space-between;
      padding-left: 1em;
      padding-right: 1em;
      line-height: 1.5em;
      h4 {
        font-size: 1.1rem;
      }
    }
  }
}
</style>