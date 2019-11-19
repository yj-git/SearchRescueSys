<template>
  <div id="history-chart"></div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import echarts from "echarts";
@Component({})
export default class CaseHistoryChart extends Vue {
  mydata: any = null;
  mychart: any = null;
  mounted() {
    this.initChart();
  }
  initChart() {
    // 基于准备好的dom，初始化echarts图表
    var myself = this;
    myself.mychart = null;
    let option = {
      xAxis: {
        type: "category",
        data: [
          "19-11-01",
          "19-11-04",
          "19-11-06",
          "19-11-08",
          "19-11-10",
          "19-11-12",
          "19-11-13"
        ]
      },
      yAxis: {
        type: "value"
      },
      backgroundColor: "#2c343c",
      textStyle: {
        color: "rgba(255, 255, 255, 0.3)"
      },
      color: "rgb(65, 238, 200)",
      series: [
        {
          data: [2, 3, 9, 6, 4, 2, 1],
          type: "line"
        }
      ]
    };
    if (myself.mychart === null) {
    }
    let chart = document.getElementById("history-chart") as HTMLDivElement;
    // TODO:[*] 19-11-19
    /*
        Argument of type 'HTMLElement | null' 
        is not assignable to parameter of type 'HTMLDivElement | HTMLCanvasElement'.
         Type 'null' is not assignable to type 'HTMLDivElement | HTMLCanvasElement'.
    */
    if (chart != null) {
      myself.mychart = echarts.init(chart);
      myself.mychart.setOption(option);
    }
  }
  get computedTest() {
    return null;
  }
}
</script>
<style scoped lang="less">
#history-chart {
  height: 500px;
  width: 800px;
  //   background:rgb(65, 238, 200);
}
</style>
