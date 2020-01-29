<template>
  <div id="oil_detail" class="card mb-3 box-shadow">
    <div class="card-header">溢油数据</div>
    <div class="card-body">
      <div class="form">
        <div class="cell">
          <div class="title">时间</div>
          <div class="content">{{ oilModelDetailData.time | fortmatDate }}</div>
        </div>
        <div class="cell">
          <div class="title">中心位置</div>
          <div class="content">{{ oilModelDetailData.point }}</div>
        </div>
        <div class="cell">
          <div class="title">求解方法</div>
          <div class="content">{{ oilModelDetailData.equation }}</div>
        </div>
      </div>
      <div class="form">
        <div class="cell">
          <div class="title">风偏系数</div>
          <div class="content">
            <el-progress
              :text-inside="true"
              :stroke-width="26"
              :percentage="oilModelDetailData.windFactor"
            ></el-progress>
          </div>
        </div>
        <div class="cell">
          <div class="title">风偏角度</div>
          <div class="content">{{ oilModelDetailData.windDir }}</div>
        </div>
      </div>
      <div class="form">
        <div class="cell">
          <div class="title">模拟步长</div>
          <div class="content">{{ oilModelDetailData.simulateStep }}</div>
        </div>
        <div class="cell">
          <div class="title">输出步长</div>
          <div class="content">{{ oilModelDetailData.consoleStep }}</div>
        </div>
      </div>
      <div class="form">
        <div class="cell">
          <div class="title">流畅不确定性</div>
          <div class="content">
            <el-progress
              :text-inside="true"
              :stroke-width="26"
              :percentage="oilModelDetailData.currentIndeterminacy"
            ></el-progress>
          </div>
        </div>
        <div class="cell">
          <div class="title">风场不确定性</div>
          <div class="content">
            <el-progress
              :text-inside="true"
              :stroke-width="26"
              :percentage="oilModelDetailData.windIndeterminacy"
            ></el-progress>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { OilModelDetailMidModel } from "@/middle_model/oil";
import moment from "moment";
@Component({
  filters: {
    fortmatDate(now: Date) {
      return moment(now).format("YYYY-MM-DD HH");
    }
  }
})
export default class OilModelDetailForm extends Vue {
  get computedTest() {
    return null;
  }
  public mydata: any = null;

  @Prop(Object)
  private oilModelDetailData!: OilModelDetailMidModel;
  public mounted() {
    // let temp = new OilModelDetailMidModel();
  }
}
</script>
<style scoped lang="less">
@import "../../styles/base";

#myform {
  /* border: 2px solid white; */
  display: inline-block;
  background: rgba(0, 0, 255, 0.829);
  text-align: center;
  color: aliceblue;
  box-shadow: 10px 10px 5px #888888;
  box-shadow: 0 0 10px whitesmoke;
  /* 边角圆滑处理 */
  border-radius: 10px;
}
#oil_detail {
  font-size: 0.7em;
  margin-bottom: 7px !important;
  @formbox();
}
#oil_detail .card-header {
  background: #125a8abd;
  /* background: linear-gradient(rgb(150, 210, 225), rgb(93, 134, 181)); */
  /* background: rgb(49, 159, 178); */
  color: rgb(161, 251, 246);
  text-shadow: 2px 2px 1px 5px rgb(161, 251, 246);
  font-weight: 400;
  padding-top: 7px;
  padding-bottom: 7px !important;
}

#oil_detail .card-body {
  /* background: #2367e4bd; */
  /* background: rgb(45, 93, 133); */
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));

  color: rgb(240, 237, 56);
  font-weight: 500;

  padding-bottom: 5px;
  padding-top: 5px;
  @bottomradius();
  display: flex;
  flex-direction: column;
  .form {
    display: flex;
  }
}

#oil_detail .card-header {
  text-align: center;
  text-shadow: 4px 4px 15px rgb(216, 57, 57);
}

.row {
  text-align: center;
  text-shadow: 2px 2px 8px rgb(210, 214, 155);
  margin-bottom: 5px;
}
</style>
