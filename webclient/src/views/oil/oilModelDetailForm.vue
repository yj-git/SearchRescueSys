<template>
  <div id="oil_detail" class="card mb-3 box-shadow">
    <div class="card-header">溢油数据</div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">时间</div>
        <div class="col-md-6">{{oilModelDetailData.time|fortmatDate}}</div>
      </div>
      <div class="row">
        <div class="col-md-6">中心位置</div>
        <div class="col-md-6">{{oilModelDetailData.point}}</div>
      </div>
      <div class="row">
        <div class="col-md-6">风偏系数</div>
        <div class="col-md-6">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="oilModelDetailData.windFactor"
          ></el-progress>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">风偏角度</div>
        <div class="col-md-6">{{oilModelDetailData.windDir}}</div>
      </div>
      <div class="row">
        <div class="col-md-6">模拟步长</div>
        <div class="col-md-6">{{oilModelDetailData.simulateStep}}</div>
      </div>
      <div class="row">
        <div class="col-md-6">输出步长</div>
        <div class="col-md-6">{{oilModelDetailData.consoleStep}}</div>
      </div>
      <div class="row">
        <div class="col-md-6">流场不确定性</div>
        <div class="col-md-6">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="oilModelDetailData.currentIndeterminacy"
          ></el-progress>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">风场不确定性</div>
        <div class="col-md-6">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="oilModelDetailData.windIndeterminacy"
          ></el-progress>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">求解方法</div>
        <div class="col-md-6">{{oilModelDetailData.equation}}</div>
      </div>
    </div>
  </div>
</template>
<script lang='ts'>
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
<style scoped>
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
}
#oil_detail .card-header {
  background: #125a8abd;
  /* background: linear-gradient(rgb(150, 210, 225), rgb(93, 134, 181)); */
  /* background: rgb(49, 159, 178); */
  color: rgb(161, 251, 246);
  text-shadow: 2px 2px 1px 5px rgb(161, 251, 246);
  font-weight: 400;
}

#oil_detail .card-body {
  /* background: #2367e4bd; */
  /* background: rgb(45, 93, 133); */
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));

  color: rgb(240, 237, 56);
  font-weight: 500;
  /* 底部圆角 */
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

#myform .table {
  margin-bottom: 0px;
}

.surge {
  background: yellow;
  color: rgb(0, 80, 251);
}

.tide {
  background: red;
}

#myform table tr td {
  width: 50;
}

.card-header {
  text-align: center;
  text-shadow: 4px 4px 15px rgb(216, 57, 57);
}

.row {
  text-align: center;
  text-shadow: 2px 2px 8px rgb(210, 214, 155);
  margin-bottom: 10px;
}

/* 注意card有一个左右15px的padding */
.card {
  /* padding-left: 0px;
  padding-right: 0px; */
  /* 需要去掉bt自带的1px的边框 */
  border: 0px;
}

.row_footer {
  margin-left: -21px;
  margin-right: -21px;
  margin-bottom: -21px;
}

/* 底部div */
.typhoon_footer {
  display: flex;
  flex-direction: row;
  background: #0044cc;
  width: 100%;
  color: white;
  /* border: 1px; */
  text-align: center;
  /* 设置圆角 */
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  /* margin-left: -21px;
				margin-right: -21px; */
}

.my_primary {
  color: white;
  background-color: #007bff;
}

.my_success {
  color: white;
  background-color: #28a745;
}

.my_info {
  color: white;
  background-color: #17a2b8;
}

.my_danger {
  color: white;
  background-color: #dc3545;
}

.typhoon_footer .columnar {
  display: flex;
  width: 50%;
  flex-direction: column;
  /* 去掉底部footer右侧的边框 */
  /* border-right: 1px solid #0000ff; */
}

.typhoon_footer .columnar .main_val {
  display: flex;
  justify-content: center;
  width: 100%;
  text-align: center;
  font-size: 20px;
}

.typhoon_footer .columnar .vice_vak {
  display: flex;
  width: 100%;
  justify-content: center;
  text-align: center;
  font-size: 0.625rem;
}
</style>