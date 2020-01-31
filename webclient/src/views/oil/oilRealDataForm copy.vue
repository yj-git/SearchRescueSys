<template>
  <div id="oil_detail" class="card mb-3 box-shadow">
    <!-- <div class="card-header">溢油数据</div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-4">时间</div>
        <div class="col-md-8">{{ oilRealData.time | fortmatDate }}</div>
      </div>
      <div class="row">
        <div class="col-md-4">中心位置</div>
        <div class="col-md-8">{{ oilRealData.point }}</div>
      </div>
      <div class="row row_footer">
        <div class="typhoon_footer">
          <div class="columnar my_primary">
            <div class="main_val">{{ oilRealData.windVal }}</div>
            <div class="vice_vak">风速</div>
          </div>
          <div class="columnar my_success">
            <div class="main_val">{{ oilRealData.windDir }}</div>
            <div class="vice_vak">风向</div>
          </div>
          <div class="columnar my_info">
            <div class="main_val">{{ oilRealData.currentVal }}</div>
            <div class="vice_vak">流速</div>
          </div>
          <div class="columnar my_danger">
            <div class="main_val">{{ oilRealData.currentDir }}</div>
            <div class="vice_vak">流向</div>
          </div>
        </div>
      </div>
    </div> -->
    <div id="oil_detail" class="mb-3 box-shadow">
      <div class="card-header">实时数据</div>
      <div class="card-body">
        <div class="form">
          <div class="cell">
            <div class="title">时间</div>
            <div class="content">
              2020-01-28 17
            </div>
          </div>
          <div class="cell">
            <div class="title">中心位置</div>
            <div class="content">120, 95</div>
          </div>
        </div>
        <div class="form">
          <div class="cell">
            <div class="title">风速</div>
            <div class="content my-font-primary">
              5.21
            </div>
          </div>
          <div class="cell">
            <div class="title">风向</div>
            <div class="content my-font-primary">-128.34</div>
          </div>
        </div>
        <div class="form">
          <div class="cell">
            <div class="title">流速</div>
            <div class="content my-font-primary">
              0.33
            </div>
          </div>
          <div class="cell">
            <div class="title">流向</div>
            <div class="content my-font-primary">45</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { OilMidModel } from '@/middle_model/oil'
import moment from 'moment'
@Component({
  filters: {
    fortmatDate(now: Date) {
      return moment(now).format('YYYY-MM-DD HH')
    }
  }
})
export default class OilRealDataForm extends Vue {
  get computedTest() {
    return null
  }
  public mydata: any = null
  @Prop(Object)
  private oilRealData!: OilMidModel
  public mounted() {}
}
</script>
<style scoped lang="less">
@import '../../styles/base';
#oil_detail {
  /* width: 200px; */
  font-size: 0.7em;
  margin-bottom: 7px !important;

  @formbox();
  // @center();
  // @test();
}
#oil_detail .card-header {
  background: #125a8abd;
  /* background: linear-gradient(rgb(150, 210, 225), rgb(93, 134, 181)); */
  /* background: rgb(49, 159, 178); */
  /* background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89)); */
  color: rgb(161, 251, 246);
  text-shadow: 2px 2px 2px 10px rgb(161, 251, 246);
  font-weight: 400;
  padding-top: 7px;
  padding-bottom: 7px !important;
}

#oil_detail .card-body {
  /* background: #2367e4bd; */
  /* background: rgb(45, 93, 133); */
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));
  color: rgb(161, 251, 246);
  /* 底部圆角 */
  @bottomradius();
  padding-top: 5px;
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
  text-shadow: 2px 2px 10px rgb(210, 214, 155);
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
  /* 底部圆角 */
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
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
  /* border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px; */
  /* margin-left: -21px;
				margin-right: -21px; */
  /* 底部圆角 */
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}
.typhoon_footer .columnar:first-child {
  /* 底部最左侧圆角 */
  border-bottom-left-radius: 10px;
}
.typhoon_footer .columnar:last-child {
  /* 底部最右侧圆角 */
  border-bottom-right-radius: 10px;
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
