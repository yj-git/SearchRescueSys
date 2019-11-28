<template>
  <div class="databox-content">
    <!-- 空间信息 -->
    <DataBox :modelData="getGisData()" :title="'空间信息'"></DataBox>
    <!-- model信息 -->
    <DataBox :modelData="getModelFactorData()" :title="'模型信息'"></DataBox>
    <DataBox :modelData="getModelEquationData()" :title="'模型信息'"></DataBox>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import DataBox from "@/views/members/form/DataBox.vue";
import { OilMidModel, OilModelDetailMidModel } from "@/middle_model/oil";

import { OilEquation } from "@/enum/Equation";
import { formatDate, getDaysNum } from "@/common/date";
@Component({
  components: {
    DataBox
  }
})
export default class OilTopModels extends Vue {
  mydata: any = null;
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

  mounted() {}
  get computedTest() {
    return null;
  }
  getGisData(): { title: string; val: string }[] {
    let dateStr = formatDate(this.oilModelDetailData.time);
    let listData: { title: string; val: string }[] = [
      {
        title: "时间",
        val: "dateStr"
      },
      {
        title: "位置",
        val: this.oilModelDetailData.point.toString()
      }
    ];
    return listData;
  }
  getModelFactorData(): { title: string; val: string }[] {
    let listData: { title: string; val: string }[] = [
      {
        title: "风偏系数",
        val: this.oilModelDetailData.windFactor.toString()
      },
      {
        title: "风偏角度",
        val: this.oilModelDetailData.windDir.toString()
      },
      {
        title: "模拟步长",
        val: this.oilModelDetailData.simulateStep.toString()
      },
      {
        title: "输出步长",
        val: this.oilModelDetailData.consoleStep.toString()
      }
    ];
    return listData;
  }

  getModelEquationData(): { title: string; val: string }[] {
    let listData: { title: string; val: string }[] = [
      {
        title: "流场不确定性",
        val: this.oilModelDetailData.currentIndeterminacy.toString()
      },
      {
        title: "风场不确定性",
        val: this.oilModelDetailData.windIndeterminacy.toString()
      },
      {
        title: "求解方法",
        val: this.oilModelDetailData.equation.toString()
      }
    ];
    return listData;
  }
}
</script>
<style scoped lang="less">
.databox-content {
  width: 98%;
}
</style>