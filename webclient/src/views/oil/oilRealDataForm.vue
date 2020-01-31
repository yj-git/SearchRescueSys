<template>
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
  @base_font();
  font-size: 0.7em;
  margin-bottom: 7px !important;
  //   @formbox();
  // 加入四个角的圆角+阴影
  border-top-left-radius: 15px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  box-shadow: 2px 2px 10px rgba(41, 101, 141, 0.863);
  // box-shadow: 2px 2px 10px rgb(109, 96, 96);
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));
}
// 两种字体颜色
.my-font-primary {
  color: rgb(255, 255, 255);
}
.my-font-contrast {
  color: rgb(206, 201, 45);
}
@base_font: {
  text-shadow: 2px 2px 8px rgb(33, 32, 32);
};
#oil_detail .card-header {
  // background: #125a8abd;
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
  // background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));

  color: rgb(240, 237, 56);
  font-weight: 500;

  padding-bottom: 5px;
  padding-top: 5px;
  //   @bottomradius();
  display: flex;
  flex-direction: column;
  .form {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 0.75em;
    .cell {
      width: 50%;
    }
    .title {
      flex: 1;
      font-size: 90%;
      font-weight: 500;
      color: aliceblue;
    }
    .content {
      flex: 2;
      display: flex;
      /* 主轴对其方式 */
      justify-content: center;
      /* 交叉轴对其方式 */
      align-items: center;
      font-size: 120%;
      font-weight: 600;
    }
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
