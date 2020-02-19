<template>
    <div id="rescue_map">
        <div id="map_content">
            <l-map ref="basemap" :zoom="zoom" :center="center">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-polyline
                    :lat-lngs="polyline.latlngs"
                    :fill="false"
                    :color="polyline.color"
                ></l-polyline>
                <l-circle
                    v-for="temp in oilAvgPointList"
                    :key="temp.id"
                    :lat-lng="temp.latlon"
                    @click="testOnOver(temp)"
                />
                <!-- <LeafletHeatmap :lat-lng="oilHeatmapList" :radius="15"></LeafletHeatmap> -->
                <!-- TODO:[*] 19-10-16 注意若动态的添加latlng的话会报错 -->
                <!-- 参考的错误如下：
        https://github.com/jurb/vue2-leaflet-heatmap/issues/2-->
                <!-- 使用的插件：
        https://github.com/jurb/vue2-leaflet-heatmap-->
                <!-- <LeafletHeatmap
        :lat-lng="oilHeatmapList"
        :radius="60"
        :min-opacity=".75"
        :max-zoom="10"
        :blur="60"
        ></LeafletHeatmap>-->
                <!-- <l-circle v-for="temp in oilScatterPointList" :key="temp.id" :lat-lng="temp" /> -->
            </l-map>
            <TimeBar :targetDate="startDate" :days="days" :interval="interval"></TimeBar>
            <div id="process">
                <!-- TODO:[-] 20-01-27 使用eu的进度条 -->
                <!-- <el-progress
          :text-inside="true"
          :stroke-width="18"
          :percentage="processOptions.rate"
        ></el-progress> -->
                <!-- 使用bt的进度条 -->
                <!-- <div
          class="progress-bar progress-bar-striped progress-bar-animated"
          role="progressbar"
          aria-valuenow="{{processOptions.rate}}"
          aria-valuemin="0"
          aria-valuemax="100"
          style="width: 75%"
        ></div> -->
                <!-- 使用bootstrap-vue的组件 -->
                <b-progress
                    :value="processOptions.rate"
                    :max="100"
                    show-progress
                    animated
                ></b-progress>
            </div>
        </div>
        <div id="right_bar">
            <!-- TODO:[*] 19-10-28 加入右侧信息栏_v1版本 -->
            <OilRightBar
                :oilRealData="oilAvgRealData"
                :days="days"
                :startDate="startDate"
                :interval="interval"
                :targetDate="current"
                :numsData="processOptions.num"
            ></OilRightBar>
        </div>

        <div class="left_select">
            <OilFactorSelect></OilFactorSelect>
            <CurdBtn :caseList="caseList"></CurdBtn>
        </div>
        <!-- TODO:[-] 20-01-27 在地图页面加入创建等的btn -->
        <div id="toolbar_btns">
            <!-- <CurdBtn></CurdBtn> -->
        </div>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import * as L from 'leaflet'
// TODO:[*] 19-10-16 加入vue2 leaflet heatmap不使用以下的方式
// import { HeatmapOverlay } from "heatmap.js";

import { Getter, Mutation, State, namespace } from 'vuex-class'
import {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LPolyline,
    LCircle,
    LIcon,
    LWMSTileLayer
    // LeafletHeatmap
} from 'vue2-leaflet'
// import LeafletHeatmap from "vue2-leaflet-heatmap";

// github:https://github.com/Leaflet/Leaflet.heat
// npm:https://www.npmjs.com/package/leaflet.heat
// import {}  "leaflet.heat";
// 注意此处的引用方式，极其蛋疼
import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap'

// 此种方式较为繁琐：https://www.patrick-wied.at/static/heatmapjs/example-heatmap-leaflet.html
import 'heatmap.js'
import TimeBar from '@/views/members/bar/TimeBar.vue'
import RightDetailBar from '@/views/members/bar/rightBarDetail.vue'
import RightOilBar from '@/views/members/bar/rightOilBar.vue'
import OilRightBar from '@/views/bar/oilRightBar.vue'
import OilFactorSelect from '@/views/members/select/OilFactorSelect.vue'
import CurdBtn from '@/views/members/tools/CurdBtn.vue'
import {
    loadOilSpillingAvgTrackList,
    loadOilScatterTrackListPage,
    loadOilRealData,
    loadOilSpillingAvgRealData,
    getTargetCodeDateRange,
    getTargetTimeTrackCount
} from '@/api/api'

// TODO:[-] 20-01-23 尝试将oil的部分操作放在oil 类中()
import { Oil, IOptions } from './oil'

import { OilPointRealDataMidModel } from '@/middle_model/rescue'
import { OilMidModel } from '@/middle_model/oil'
import { ICaseMin, CaseMinInfo, CaseOilModel } from '@/middle_model/case'
import { getDaysNum } from '@/common/date'

// 引入常量
import { optionsFactors, optionsShowTypes } from '@/const/Oil'
import { OilFactor, ShowType } from '@/enum/OilSelect'
import { Case, CaseModelInfo } from '@/views/content/oilspilling/case'
@Component({
    components: {
        'l-marker': LMarker,
        'l-map': LMap,
        'l-tile-layer': LTileLayer,
        'l-polyline': LPolyline,
        'l-circle': LCircle,
        'l-icon': LIcon,
        TimeBar,
        RightDetailBar,
        RightOilBar,
        OilRightBar,
        OilFactorSelect,
        CurdBtn
        // LeafletHeatmap
    }
})
export default class OilSpillingMap extends Vue {
    mydata: any = null
    code = 'sanjioil'
    zoom = 5
    center: any = [17.6, 131.6]
    url =
        '//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}'
    // 指定时间
    // targetDate: Date = new Date();
    // 溢油平均轨迹
    oilAvgPointList: Array<OilPointRealDataMidModel> = []
    // TODO:[*] 19-10-31 由于设置类型为any，且赋值为null，引发的子组件在为null的情况下未渲染
    oilAvgRealData: OilMidModel = new OilMidModel()
    // 指定时刻的全部轨迹散点数组
    oilScatterPointList: Array<number[]> = []
    oilScatterCircleList: Array<any> = []
    oilHeatmapList: Array<any> = []
    polyline: {
        latlngs: []
        color: string
    } = {
        latlngs: [],
        color: 'yellow'
    }

    // TODO:[*] 19-11-04 heatLayer 当前的热图layer
    tempHeatLayer: any = null

    // 当前选定的 case model 信息
    tempCaseModel: CaseOilModel
    // timebar的起始时间
    // TODO:[*] 19-11-07 去掉默认的起始时间
    startDate: Date = new Date()
    targetDate: Date = new Date()
    finishDate: Date = new Date()
    interval = 24
    // timebar共有多少天
    days = 3

    tempOilDivIcon: any = null
    tempOil: any = null
    // TODO:[*] 19-11-12 加入show type与show factor
    showType: number
    showFactor: number
    // TODO:[*] 20-01-27 与进度相关的options
    processOptions: { rate: number; num: { current: number; sum: number } } = {
        rate: 0,
        num: { current: 0, sum: 0 }
    }
    caseList: CaseMinInfo[] = []
    created() {
        this.startDate = new Date()
        this.targetDate = new Date()

        // TODO:[*] 19-11-05:页面加载时需要获取当前code对应的旗帜时间
        this.loadDateRange()
    }

    mounted() {
        // 由于是测试，页面加载完成后先加载当前 code 的平均轨迹
        // TODO:[*] 20-01-23 暂时去掉页面加载后读取平均轨迹的步骤(暂时去掉)
        // this.loadTrackAvgList();
        // TODO:[*] 19-11-07 将loadDate的操作放在created中
        // this.startDate = new Date(2018, 0, 14, 22, 20);
        // // TODO:[*] 19-11-05:页面加载时需要获取当前code对应的旗帜时间
        // this.loadDateRange();
        // TODO:[-] 20-02-18 页面加载完成先加载历史case list
        // console.log(caseList)
        this.loadCaseList()
    }
    loadCaseList() {
        this.clearCaseList()
        const productType = this.$store.getters['common/productType']
        const caseList: CaseMinInfo[] = []
        const caseFactory = new Case(productType)
        caseFactory.getCaseListByUser().then((res) => {
            console.log(`获取到上面的promise传给的 CaseMinInfo[]:${res}`)
            this.caseList = res
        })
    }
    clearCaseList() {
        this.caseList = []
    }
    // 加载指定code的平均轨迹
    loadTrackAvgList(): void {
        const myself = this
        loadOilSpillingAvgTrackList(this.code).then((res) => {
            if (res.status === 200) {
                res.data.forEach((temp: any) => {
                    myself.oilAvgPointList.push(
                        new OilPointRealDataMidModel(
                            [temp.point.coordinates[1], temp.point.coordinates[0]],
                            new Date(temp.time)
                        )
                    )
                    this.polyline.latlngs.push([
                        temp.point.coordinates[1],
                        temp.point.coordinates[0]
                    ])
                })
            }
        })
    }
    // 根据当前选中的时间加载该时间的全部溢油 散点轨迹
    loadTrackHeatmap(code: string, dt: Date, index: number, count: number): void {
        const myself = this
        //TODO:[*] 19-11-13 清除统一放在clearAllLayer中，此处暂时注释掉
        // this.clearScatterPoint();
        const mymap: any = this.$refs.basemap['mapObject']
        this.oilHeatmapList = []
        //TODO:[*] 19-11-04 清除layerHeat
        this.clearHeatLayer()
        // TODO:[*] 19-10-16 尝试加入热力图的效果
        // TODO:[*] 20-01-23 注意此处由直接调用当前的vue中的data取值，改为由方法参数取值
        loadOilScatterTrackListPage(code, dt, index, count).then((res) => {
            if (res.status === 200) {
                // TODO : [*] 19-09-25 注意此处 使用leaflet2vue插件会导致vue的组件崩溃。
                // 尝试使用直接添加的方式
                res.data.forEach((temp: any) => {
                    this.oilScatterPointList.push([
                        temp.point.coordinates[1],
                        temp.point.coordinates[0]
                    ])

                    this.oilHeatmapList.push({
                        lat: temp.point.coordinates[1],
                        lng: temp.point.coordinates[0],
                        count: 2
                    })

                    // todo:[*] 19-10-16 暂时去掉散点，只保留热图
                    // let temp_circle = L.circle(
                    //   [temp.point.coordinates[1], temp.point.coordinates[0]],
                    //   {
                    //     radius: 30
                    //   }
                    // ).addTo(mymap);

                    // this.oilScatterCircleList.push(temp_circle);
                })
                // 获取到当前的map

                // 对应的是Leaflet.heat库
                // 但是会提示：Property 'heatLayer' does not exist on type 'typeof import("D:/02proj/SearchRescue/SearchRescueSys/webclient/node_modules/@types/leaflet/index")'.
                const list = this.oilHeatmapList

                const testData = {
                    max: 2,
                    data: list
                }
                const cfg = {
                    radius: 0.01,
                    maxOpacity: 0.8,
                    scaleRadius: true,
                    useLocalExtrema: true,
                    latField: 'lat',
                    lngField: 'lng',
                    valueField: 'count'
                }
                const heatLayer = new HeatmapOverlay(cfg)

                heatLayer.setData(testData)
                // TODO:[*] 19-11-04 添加完heatlayer后，再次更新时记得需要remove
                myself.tempHeatLayer = heatLayer
                heatLayer.addTo(mymap)
            }
        })
    }

    // 加载散点图
    loadTrackScatterPoint(code: string, dt: Date, index: number, count: number): void {
        const myself = this
        //TODO:[*] 19-11-13 清除统一放在clearAllLayer中，此处暂时注释掉
        // this.clearScatterPoint();
        const mymap: any = this.$refs.basemap['mapObject']

        // TODO:[*] 20-01-23 注意此处由直接调用当前的vue中的data取值，改为由方法参数取值
        loadOilScatterTrackListPage(code, dt, index, count).then((res) => {
            if (res.status === 200) {
                // TODO : [*] 19-09-25 注意此处 使用leaflet2vue插件会导致vue的组件崩溃。
                // 尝试使用直接添加的方式
                res.data.forEach((temp: any) => {
                    this.oilScatterPointList.push([
                        temp.point.coordinates[1],
                        temp.point.coordinates[0]
                    ])

                    // todo:[*] 19-10-16 暂时去掉散点，只保留热图
                    const temp_circle = L.circle(
                        [temp.point.coordinates[1], temp.point.coordinates[0]],
                        {
                            radius: 30
                        }
                    ).addTo(mymap)

                    this.oilScatterCircleList.push(temp_circle)
                })
                // 加载当前的current
                myself.processOptions.num.current =
                    myself.processOptions.num.current + res.data.length
            }
        })
    }

    loadTargetCaseModel(code: string) {
        const tempCase: CaseModelInfo = new CaseModelInfo(code)
        tempCase.getCaseModelInfo(code).then((res) => {
            console.log(res)
        })
    }
    clearAllLayer(): void {
        this.clearOilAvgPolyLine()
        this.clearOilAvgPointList()
        this.clearScatterPoint()
        this.clearHeatLayer()
    }

    clearScatterPoint(): void {
        const mymap: any = this.$refs.basemap['mapObject']
        this.oilScatterPointList = []
        this.oilScatterCircleList.forEach((temp) => {
            mymap.removeLayer(temp)
        })
    }

    clearHeatLayer(): void {
        const mymap: any = this.$refs.basemap['mapObject']
        //去除掉heatlayer
        if (this.tempHeatLayer != null) {
            mymap.removeLayer(this.tempHeatLayer)
        }
    }
    // 清除与point与poly相关
    clearOilAvgPointList(): void {
        this.oilAvgPointList = []
    }
    clearOilAvgPolyLine(): void {
        this.polyline.latlngs = []
    }

    testOnOver(temp: OilPointRealDataMidModel): void {
        // console.log("鼠标移入点");
        if (this.tempOilDivIcon != null) {
            this.clearOilDivFromMap()
        }
        // console.log(temp);
        loadOilRealData(this.code, temp.date).then((res) => {
            if (res.status === 200) {
                // console.log(res);
                const tempData = res.data
                const oilTemp = new OilMidModel(
                    tempData['time'],
                    tempData['status'],
                    tempData['code'],
                    tempData['point']['coordinates'],
                    tempData['current'],
                    tempData['wind']
                )
                this.tempOil = oilTemp
                // this.addOilDiv2Map(oilTemp);
            }
        })
        // 鼠标移入散点之后加载详细数据的div
        // 需要向后台发送请求，parms有 date，code
    }
    // 向地图中添加溢油详细数据的div
    addOilDiv2Map(tempOil: OilMidModel): void {
        const myself = this
        const baseMap: any = this.$refs.basemap
        const myMap: any = baseMap['mapObject']
        const oilDivHtml = tempOil.toDivHtml()
        const oilDivIcon = L.divIcon({
            className: 'oil_icon_default',
            html: oilDivHtml,
            // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
            iconAnchor: [-20, 30]
        })

        const oilDivIconTemp = L.marker([tempOil.latlon[1], tempOil.latlon[0]], {
            icon: oilDivIcon
        }).addTo(myMap)
        // console.log("将divIcon插入map中");
        myself.tempOilDivIcon = oilDivIconTemp
    }

    loadTargetRealData(code: string, date: Date) {
        const myself = this
        loadOilSpillingAvgRealData(code, date).then((res) => {
            if (res.status === 200) {
                // console.log(res.data);
                const data = res.data
                myself.oilAvgRealData = new OilMidModel(
                    data['time'],
                    data['status'],
                    data['code'],
                    data['coordinates'],
                    data['current'],
                    data['wind']
                )
            }
        })
    }

    // TODO:[*] 19-11-05 根据当前的 code 获取oil avg的起止时间
    loadDateRange(): void {
        const myself = this
        getTargetCodeDateRange(this.code).then((res) => {
            if (res.status === 200) {
                // 获取起止时间
                const start = new Date(res.data['start'])
                const end = new Date(res.data['end'])
                /*
          下面需要获取：
                [ ] -1 有多少天
                [ ] -2 起始时间
                [ ] -3 每天的格子数量

        */
                // console.log(res);
                const daysCount = getDaysNum(start, end)
                myself.days = daysCount
                myself.startDate = start
                myself.finishDate = end
                // TODO:[*] 19-11-07 此处每次获取完start之后，先赋值给current，之后再由timebar选择之后再更新
                myself.targetDate = start
            }
        })
    }

    // 将当前的溢油数据的div从map中移出
    clearOilDivFromMap(): void {
        // console.log("鼠标移出");
        const myself = this
        const mymap: any = this.$refs.basemap['mapObject']
        mymap.removeLayer(myself.tempOilDivIcon)
        myself.tempOilDivIcon = null
    }
    get computedTest() {
        return null
    }

    // TODO:[*] 19-11-12 不再使用此种方式，暂时注释掉
    get current(): Date {
        // TODO:[*] 19-11-07 注意此处的current为string类型（含时区），需要再转换为date
        // return ;

        // let currentStr: string = this.$store.state.current;
        const currentStr: string = this.getcurrent

        let currentDt: Date = new Date()
        if (currentStr != '') {
            currentDt = new Date(currentStr)
        }
        return currentDt
    }

    // TODO:[*] 19-11-08 使用vuex-clas的方式监听oil 的两个select
    @Getter('getShowFactor', { namespace: 'oil' }) getShowFactor
    @Watch('getShowFactor')
    OnShowFactor(val: number) {
        // console.log(`监听到vuex中namespace:oil factor发生变化:${val}`);
        this.showFactor = val
        // TODO:[*] 20-01-23 此处暂时注释掉对于factor改变后应该加载的业务逻辑
        // this.loadTrackFactory();
    }

    // TODO:[*] 19-11-12 根据 current showType showFactor决定的加载的layer
    loadTrackFactory(count: number): void {
        const val: number = this.showType
        // TODO:[*] 19-11-13 加入了clear方法，清除散点以及热图（或放在各个load方法中）
        this.clearAllLayer()
        const oilCls = new Oil({
            code: this.code,
            dt: this.targetDate,
            interval: 1000,
            pageCount: 200
        })
        switch (val) {
            // 散点
            case ShowType.SCATTER:
                // 切换为散点视图
                // TODO:[-] 20-01-23 此处放弃读取散点的原先方式，改为直接调用oil.ts的方法的方式
                // this.loadTrackScatterPoint();
                oilCls.intervalLoadTracks(count, this.loadTrackScatterPoint, this.processOptions)
                break
            case ShowType.HEATMAP:
                // 切换为热图视图
                // TODO:[*] 20-01-23 此处改为和上面的加载散点的相同的方式
                // 20-01-23 原始版本注释掉
                // this.loadTrackHeatmap();
                oilCls.intervalLoadTracks(count, this.loadTrackHeatmap, this.processOptions)
                break
        }
    }

    @Getter('casecode', { namespace: 'case' }) casecode: string
    @Watch('casecode')
    onCaseCode(val: string): void {
        console.log(`监听到store中的case code 变化 :${val}`)
        this.code = val
        // 清除当前的散点
        this.clearAllLayer()
        // 调用加载指定code的平均轨迹的方法
        this.loadTrackAvgList()
    }

    @Getter('getShowType', { namespace: 'oil' }) getShowType: number
    @Watch('getShowType')
    onShowType(val: number) {
        // console.log(`监听到vuex中namespace:oil type发生变化:${val}`);
        this.showType = val
    }

    @Watch('tempOil')
    onOil(oil: OilMidModel) {
        // console.log(`监听oil发生变化，现值为${this.tempOil}`);
    }

    @Watch('processOptions.rate')
    onProcessOptions(rate: number) {
        console.log(`监听到processOptions发生变化:${rate}`)
    }

    @Getter('getCurrent', { namespace: 'map' }) getcurrent
    @Watch('current')
    onCurrent(val: Date): void {
        const myself = this
        this.targetDate = new Date(val)
        // TODO:[*] 20-01-23 选定时间更新后先获取当前时间的散点总数
        getTargetTimeTrackCount(this.code, val).then((res) => {
            if (res.status === 200) {
                const trackCount = res.data
                // TODO:[-] 20-02-01 将散点的总数赋值给options
                myself.processOptions.num.sum = trackCount
                this.loadTrackFactory(trackCount) // TODO:[*] 19-11-12 调用修改后的loadTrack 工厂方法

                // TODO:[*] 20-01-23 根据获取的当前时间的散点的数量，执行分页请求
                // 先加载oil 的realdata，再加载热力图
                this.loadTargetRealData(myself.code, myself.targetDate)
                // TODO:[*] 19-10-31 此处需要加入一个切换的功能
                // this.loadTrackFactory()
                // this.loadTrackHeatmap();
            }
        })
    }
}
</script>
<style scoped lang="less">
// TODO:[*] 19-11-13 注意引入less时不需要加.less后缀
@import '../../../styles/base';
#rescue_map {
    /* height: 100%; */
    /* display: flex;
  flex-direction: column; */
    @center();
    // @test();
    // display: flex;
    // flex: 22;
    // height: 86vh;
    /* width: 1500px;
  height: 700px; */
    /* background: #2a79d4; */

    // 左侧的切换按钮
    .left_select {
        position: absolute;
        top: 150px;
        left: 50px;
        z-index: 1500;
        display: flex;
    }

    #toolbar_btns {
        position: absolute;
        top: 17em;
        // left: 10em;
        z-index: 1500;
        width: 70%;
    }
}
#map_content {
    // 此处放在base.less中的@centermap中
    // padding: 10px;
    flex: 5;
    display: flex;
    flex-direction: column;
    @centermap();
    #process {
        display: flex;
        z-index: 1500;
        width: 100%;
        .progress {
            width: 100%;
        }
        // margin-right: 10rem;
        // position: absolute;
        // bottom: 8rem;
        // left: 12rem;
        // width: 15em;
    }
}
#right_bar {
    flex: 1;
    margin-right: 10px;

    padding: 10px;
    /* background: rgba(188, 143, 143, 0.507); */
}
#rescue_map .vue2leaflet-map {
    /* display: flex;
  flex-direction: column;
  flex: 24; */
    display: flex;
    flex: 1;
    /* 底部圆角 */
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
// 加载散点的进度条

.oil_icon_default {
    width: 750px !important;
    z-index: 1700 !important;
}
.typhoon_data_div .row {
    color: white;
}

.typhoon_data_div .card-body {
    color: white;
}

.typhoon_data_div {
    z-index: 10000;
    color: white;
    padding-left: 0px !important;
    padding-right: 0px !important;
    background: linear-gradient(to right, #1a6865 30%, rgba(4, 107, 114, 0.103));
}

#oil_div {
    z-index: 2000;
}

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
    border-right: 1px solid #0000ff;
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
