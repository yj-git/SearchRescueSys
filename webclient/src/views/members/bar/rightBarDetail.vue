<template>
  <div id="oil_detail" class="card mb-4 col-md-4 box-shadow">
    <div class="card-header">溢油数据</div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-4">时间</div>
        <div class="col-md-8">{{ oil.time }}</div>
      </div>
      <div class="row">
        <div class="col-md-4">中心位置</div>
        <div class="col-md-8">{{ oil.latlon }}</div>
      </div>
      <div class="row row_footer">
        <div class="typhoon_footer">
          <div class="columnar my_primary">
            <div class="main_val">{{ oil.windVal }}</div>
            <div class="vice_vak">风速</div>
          </div>
          <div class="columnar my_success">
            <div class="main_val">{{ oil.windDir | dirConvert }}</div>
            <div class="vice_vak">风向</div>
          </div>
          <div class="columnar my_info">
            <div class="main_val">{{ oil.currentVal }}</div>
            <div class="vice_vak">流速</div>
          </div>
          <div class="columnar my_danger">
            <div class="main_val">{{ oil.currentDir | dirConvert }}</div>
            <div class="vice_vak">流向</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { OilMidModel } from "@/middle_model/oil";
// import { dirConvertDec } from "@/decorator/mymath";
@Component({
  filters: {
    // 方向转换，将可能出现的负角度（第三四象限）的角度，改为正的（大于180）
    dirConvert(val: number): number {
      let res = val;
      if (val < 0) {
        res = 360 + val;
      }
      return res;
    }
  }
})
export default class RightBarDetail extends Vue {
  mydata: any = null;
  @Prop(OilMidModel) oil: OilMidModel;
  // @Prop(Object)date:Date;
  // @Prop(Array) latlon:Array<number>;
  mounted() {}
  get computedTest() {
    return null;
  }

  @Watch("oil")
  onOil(val: OilMidModel) {
    console.log(`监听到父组件传入的oil${val}`);
  }

  get windVal(): number {
    return 0;
  }
}
</script>
<style scoped>
.card-header {
  text-align: center;
  text-shadow: 2px 2px 10px grey;
}
.row {
  text-align: center;
  text-shadow: 2px 2px 10px grey;
  margin-bottom: 10px;
}
/* 注意card有一个左右15px的padding */
.card {
  padding-left: 0px;
  padding-right: 0px;
  /* 需要去掉bt自带的1px的边框 */
  border: 0px;
  background: #ffffff07;
}
.row_footer {
  margin-left: -21px;
  margin-right: -21px;
  margin-bottom: -21px;
}

#oil_detail {
  z-index: 1500;
  position: absolute;
  top: 100px;
  right: 50px;
  width: 300px;
}

#oil_detail .card-header {
  /* background: #17a3b8bd; */
  /* background: linear-gradient(rgb(150, 210, 225), rgb(93, 134, 181)); */
  background: rgba(49, 159, 178, 0.575);
  color: rgb(161, 251, 246);
  text-shadow: 2px 2px 2px 10px rgb(161, 251, 246);
  font-weight: 400;
}
#oil_detail .card-body {
  /* background: #2367e4bd; */
  background: rgba(45, 93, 133, 0.733);
  color: rgb(161, 251, 246);
}

/* 底部div */
.typhoon_footer {
  display: flex;
  flex-direction: row;
  background: #0044cc;
  width: 100%;
  color: white;
  border: 1px;
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
