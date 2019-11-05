<template>
  <div>
    <oilModelDetial :oilModelDetailData="oilModelDetailData"></oilModelDetial>
    <oilData :oilRealData="oilRealData"></oilData>
    <timeBar :step="step" :index="index" :startDate="startDate" :count="count"></timeBar>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import oilData from "@/views/oil/oilDataForm.vue";
import oilModelDetial from "@/views/oil/oilModelDetailForm.vue";
// import timeBar from "@/views/timebar/DayCardV1/DayComp.vue";
import timeBar from "@/views/members/timebar/DaysComp.vue";
import { OilMidModel, OilModelDetailMidModel } from "@/middle_model/oil";
import { OilEquation } from "@/enum/Equation";
import { XYMidMode, PointMidModel } from "@/middle_model/coordinate";
// 组件引入
@Component({ components: { oilModelDetial, oilData, timeBar } })
export default class RightInfoBar extends Vue {
  public mydata: any = null;
  public step: number = 1;
  public index: number = 3;
  public startDate: Date = new Date();
  public count: number = 72;
  // public oilRealData: OilMidModel = new OilMidModel(
  //   new Date(),
  //   1,
  //   "",
  //   [120, 95],
  //   new XYMidMode(1, 2),
  //   new XYMidMode(2, 3)
  // );
  public oilModelDetailData: OilModelDetailMidModel = new OilModelDetailMidModel(
    new Date(),
    [120, 95],
    5.2,
    215,
    120,
    120,
    72,
    81,
    OilEquation.RungeKutta
  );
  @Prop(Object)
  oilRealData!: OilMidModel;

  public mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
</style>
