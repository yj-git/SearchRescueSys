<template>
    <div id="container">
        <oilModelDetial :oilModelData="oilModelData"></oilModelDetial>
        <oilData :oilRealData="oilRealData"></oilData>
        <RangePie :leftNum="scatterLeftNum" :currentNum="numsData.current"></RangePie>
        <!-- <timeBar :step="step" :index="index" :startDate="startDate" :count="count"></timeBar> -->
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import oilData from '@/views/oil/oilRealDataForm.vue'
// TODO:[-] 20-01-28 此处修改了布局方式
// import oilModelDetial from "@/views/oil/oilModelDetailForm.vue";
import oilModelDetial from '@/views/oil/oilModelDetailForm2.vue'
// import timeBar from "@/views/timebar/DayCardV1/DayComp.vue";
import timeBar from '@/views/members/timebar/DaysComp.vue'
import RangePie from '@/views/members/pie/rangePie.vue'
import { OilMidModel, OilModelDetailMidModel } from '@/middle_model/oil'
import { CaseOilModel } from '@/middle_model/case'
import { OilEquation } from '@/enum/Equation'
import { XYMidMode, PointMidModel } from '@/middle_model/coordinate'
import moment from 'moment'
// 组件引入
@Component({ components: { oilModelDetial, oilData, timeBar, RangePie } })
export default class RightInfoBar extends Vue {
    public mydata: any = null
    // 时间 bar 的间隔
    public step = 1
    // public index: number = 3;
    // public startDate: Date = new Date();
    // public count: number = 72;
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
    )
    @Prop(Object)
    oilRealData!: OilMidModel

    // 当前vuex中选定的case code对应的 oil 模型 data
    @Prop(Object)
    oilModelData!: CaseOilModel

    @Prop(Number)
    days = 3

    @Prop(Date)
    startDate: Date

    // start: Date = this.startDate;

    @Prop(Number)
    interval = 24

    // 当前时间
    @Prop(Date)
    targetDate: Date
    @Prop(Object)
    numsData: { current: number; sum: number }
    // current: Date = this.targetDate;
    public mounted() {}
    get computedTest() {
        return null
    }

    // 获取当前的date(targetDate) 是在timebar中的第几个位置
    get index() {
        /*
        targetDate-startDate=时间差（hours)
        +
        startDate.hour
      */
        let index: number =
            (this.targetDate.getTime() - this.startDate.getTime()) /
                (1000 * 60 * 60) /
                this.timeInterval +
            this.startDate.getHours() * this.timeInterval
        index = Math.floor(index)
        return index
    }

    get timeInterval() {
        return 24 / this.interval
    }

    //
    get count() {
        return this.days * this.interval
    }

    get scatterLeftNum() {
        return this.numsData.sum - this.numsData.current
    }
}
</script>
<style scoped>
#container {
    height: 100%;
}
</style>
