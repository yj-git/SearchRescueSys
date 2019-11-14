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
      <TimeBar
        :targetDate="startDate"
        :days="days"
        :interval="interval"
      ></TimeBar>
    </div>
    <div id="right_bar">
      <!-- TODO:[*] 19-10-28 加入右侧信息栏_v1版本 -->
      <OilRightBar
        :oilRealData="oilAvgRealData"
        :days="days"
        :startDate="startDate"
        :interval="interval"
        :targetDate="current"
      ></OilRightBar>
    </div>
    <div class="left_select">
      <OilFactorSelect></OilFactorSelect>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import * as L from "leaflet";
// TODO:[*] 19-10-16 加入vue2 leaflet heatmap不使用以下的方式
// import { HeatmapOverlay } from "heatmap.js";

import { Getter, Mutation, State, namespace } from "vuex-class";
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
} from "vue2-leaflet";
// import LeafletHeatmap from "vue2-leaflet-heatmap";

// github:https://github.com/Leaflet/Leaflet.heat
// npm:https://www.npmjs.com/package/leaflet.heat
// import {}  "leaflet.heat";
// 注意此处的引用方式，极其蛋疼
import HeatmapOverlay from "heatmap.js/plugins/leaflet-heatmap";

// 此种方式较为繁琐：https://www.patrick-wied.at/static/heatmapjs/example-heatmap-leaflet.html
import "heatmap.js";
import TimeBar from "@/views/members/bar/TimeBar.vue";
import RightDetailBar from "@/views/members/bar/rightBarDetail.vue";
import RightOilBar from "@/views/members/bar/rightOilBar.vue";
import OilRightBar from "@/views/bar/oilRightBar.vue";
import OilFactorSelect from "@/views/members/select/OilFactorSelect.vue";
import {
  loadOilSpillingAvgTrackList,
  loadOilScatterTrackList,
  loadOilRealData,
  loadOilSpillingAvgRealData,
  getTargetCodeDateRange
} from "@/api/api";

import { OilPointRealDataMidModel } from "@/middle_model/rescue";
import { OilMidModel } from "@/middle_model/oil";

import { getDaysNum } from "@/common/date";

// 引入常量
import { optionsFactors, optionsShowTypes } from "@/const/Oil";
import { OilFactor, ShowType } from "@/enum/OilSelect";
@Component({
  components: {
    "l-marker": LMarker,
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-polyline": LPolyline,
    "l-circle": LCircle,
    "l-icon": LIcon,
    TimeBar,
    RightDetailBar,
    RightOilBar,
    OilRightBar,
    OilFactorSelect
    // LeafletHeatmap
  }
})
export default class OilSpillingMap extends Vue {
  mydata: any = null;
  code: string = "sanjioil";
  zoom: number = 5;
  center: any = [17.6, 131.6];
  url: string =
    "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}";
  // 指定时间
  // targetDate: Date = new Date();
  // 溢油平均轨迹
  oilAvgPointList: Array<OilPointRealDataMidModel> = [];
  // TODO:[*] 19-10-31 由于设置类型为any，且赋值为null，引发的子组件在为null的情况下未渲染
  oilAvgRealData: OilMidModel = new OilMidModel();
  // 指定时刻的全部轨迹散点数组
  oilScatterPointList: Array<number[]> = [];
  oilScatterCircleList: Array<any> = [];
  oilHeatmapList: Array<any> = [];
  polyline: any = {
    latlngs: [],
    color: "yellow"
  };

  // TODO:[*] 19-11-04 heatLayer 当前的热图layer
  tempHeatLayer: any = null;
  // timebar的起始时间
  // TODO:[*] 19-11-07 去掉默认的起始时间
  startDate: Date = new Date();
  targetDate: Date = new Date();
  interval: number = 24;
  // timebar共有多少天
  days: number = 3;

  tempOilDivIcon: any = null;
  tempOil: any = null;
  // TODO:[*] 19-11-12 加入show type与show factor
  showType: number;
  showFactor: number;
  created() {
    this.startDate = new Date();
    this.targetDate = new Date();

    // TODO:[*] 19-11-05:页面加载时需要获取当前code对应的旗帜时间
    this.loadDateRange();
  }

  mounted() {
    // 由于是测试，页面加载完成后先加载当前 code 的平均轨迹
    this.loadTrackAvgList();
    // TODO:[*] 19-11-07 将loadDate的操作放在created中
    // this.startDate = new Date(2018, 0, 14, 22, 20);
    // // TODO:[*] 19-11-05:页面加载时需要获取当前code对应的旗帜时间
    // this.loadDateRange();
  }
  // 加载指定code的平均轨迹
  loadTrackAvgList(): void {
    let myself = this;
    loadOilSpillingAvgTrackList(this.code).then(res => {
      if (res.status === 200) {
        res.data.forEach((temp: any) => {
          myself.oilAvgPointList.push(
            new OilPointRealDataMidModel(
              [temp.point.coordinates[1], temp.point.coordinates[0]],
              new Date(temp.time)
            )
          );
          this.polyline.latlngs.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);
        });
      }
      // console.log(res.data);
    });
  }
  // 根据当前选中的时间加载该时间的全部溢油 散点轨迹
  loadTrackHeatmap(): void {
    let myself = this;
    //TODO:[*] 19-11-13 清除统一放在clearAllLayer中，此处暂时注释掉
    // this.clearScatterPoint();
    let mymap: any = this.$refs.basemap["mapObject"];
    this.oilHeatmapList = [];
    //TODO:[*] 19-11-04 清除layerHeat
    this.clearHeatLayer();
    // TODO:[*] 19-10-16 尝试加入热力图的效果
    loadOilScatterTrackList(this.code, this.targetDate).then(res => {
      if (res.status === 200) {
        // TODO : [*] 19-09-25 注意此处 使用leaflet2vue插件会导致vue的组件崩溃。
        // 尝试使用直接添加的方式
        res.data.forEach((temp: any) => {
          this.oilScatterPointList.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);

          this.oilHeatmapList.push({
            lat: temp.point.coordinates[1],
            lng: temp.point.coordinates[0],
            count: 2
          });

          // todo:[*] 19-10-16 暂时去掉散点，只保留热图
          // let temp_circle = L.circle(
          //   [temp.point.coordinates[1], temp.point.coordinates[0]],
          //   {
          //     radius: 30
          //   }
          // ).addTo(mymap);

          // this.oilScatterCircleList.push(temp_circle);
        });
        // 获取到当前的map

        // 对应的是Leaflet.heat库
        // 但是会提示：Property 'heatLayer' does not exist on type 'typeof import("D:/02proj/SearchRescue/SearchRescueSys/webclient/node_modules/@types/leaflet/index")'.
        let list = this.oilHeatmapList;

        var testData = {
          max: 2,
          data: list
        };
        var cfg = {
          radius: 0.01,
          maxOpacity: 0.8,
          scaleRadius: true,
          useLocalExtrema: true,
          latField: "lat",
          lngField: "lng",
          valueField: "count"
        };
        var heatLayer = new HeatmapOverlay(cfg);

        heatLayer.setData(testData);
        // TODO:[*] 19-11-04 添加完heatlayer后，再次更新时记得需要remove
        myself.tempHeatLayer = heatLayer;
        heatLayer.addTo(mymap);
      }
    });
  }

  // 加载散点图
  loadTrackScatterPoint(): void {
    let myself = this;
    //TODO:[*] 19-11-13 清除统一放在clearAllLayer中，此处暂时注释掉
    // this.clearScatterPoint();
    let mymap: any = this.$refs.basemap["mapObject"];
    loadOilScatterTrackList(this.code, this.targetDate).then(res => {
      if (res.status === 200) {
        // TODO : [*] 19-09-25 注意此处 使用leaflet2vue插件会导致vue的组件崩溃。
        // 尝试使用直接添加的方式
        res.data.forEach((temp: any) => {
          this.oilScatterPointList.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);

          // todo:[*] 19-10-16 暂时去掉散点，只保留热图
          let temp_circle = L.circle(
            [temp.point.coordinates[1], temp.point.coordinates[0]],
            {
              radius: 30
            }
          ).addTo(mymap);

          this.oilScatterCircleList.push(temp_circle);
        });
      }
    });
  }

  clearAllLayer(): void {
    this.clearScatterPoint();
    this.clearHeatLayer();
  }

  clearScatterPoint(): void {
    let mymap: any = this.$refs.basemap["mapObject"];
    this.oilScatterPointList = [];
    this.oilScatterCircleList.forEach(temp => {
      mymap.removeLayer(temp);
    });
  }

  clearHeatLayer(): void {
    let mymap: any = this.$refs.basemap["mapObject"];
    //去除掉heatlayer
    if (this.tempHeatLayer != null) {
      mymap.removeLayer(this.tempHeatLayer);
    }
  }

  testOnOver(temp: OilPointRealDataMidModel): void {
    console.log("鼠标移入点");
    if (this.tempOilDivIcon != null) {
      this.clearOilDivFromMap();
    }
    // console.log(temp);
    loadOilRealData(this.code, temp.date).then(res => {
      if (res.status === 200) {
        console.log(res);
        let tempData = res.data;
        let oilTemp = new OilMidModel(
          tempData["time"],
          tempData["status"],
          tempData["code"],
          tempData["point"]["coordinates"],
          tempData["current"],
          tempData["wind"]
        );
        this.tempOil = oilTemp;
        // this.addOilDiv2Map(oilTemp);
      }
    });
    // 鼠标移入散点之后加载详细数据的div
    // 需要向后台发送请求，parms有 date，code
  }
  // 向地图中添加溢油详细数据的div
  addOilDiv2Map(tempOil: OilMidModel): void {
    let myself = this;
    let baseMap: any = this.$refs.basemap;
    let myMap: any = baseMap["mapObject"];
    let oilDivHtml = tempOil.toDivHtml();
    let oilDivIcon = L.divIcon({
      className: "oil_icon_default",
      html: oilDivHtml,
      // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
      iconAnchor: [-20, 30]
    });

    let oilDivIconTemp = L.marker([tempOil.latlon[1], tempOil.latlon[0]], {
      icon: oilDivIcon
    }).addTo(myMap);
    console.log("将divIcon插入map中");
    myself.tempOilDivIcon = oilDivIconTemp;
  }

  loadTargetRealData(code: string, date: Date) {
    let myself = this;
    loadOilSpillingAvgRealData(code, date).then(res => {
      if (res.status === 200) {
        console.log(res.data);
        let data = res.data;
        myself.oilAvgRealData = new OilMidModel(
          data["time"],
          data["status"],
          data["code"],
          data["coordinates"],
          data["current"],
          data["wind"]
        );
      }
    });
  }

  // TODO:[*] 19-11-05 根据当前的 code 获取oil avg的起止时间
  loadDateRange(): void {
    let myself = this;
    getTargetCodeDateRange(this.code).then(res => {
      if (res.status === 200) {
        // 获取起止时间
        let start = new Date(res.data["start"]);
        let end = new Date(res.data["end"]);
        /*
          下面需要获取：
                [ ] -1 有多少天
                [ ] -2 起始时间
                [ ] -3 每天的格子数量

        */
        console.log(res);
        let daysCount = getDaysNum(start, end);
        myself.days = daysCount;
        myself.startDate = start;
        // TODO:[*] 19-11-07 此处每次获取完start之后，先赋值给current，之后再由timebar选择之后再更新
        myself.targetDate = start;
      }
    });
  }

  // 将当前的溢油数据的div从map中移出
  clearOilDivFromMap(): void {
    console.log("鼠标移出");
    let myself = this;
    let mymap: any = this.$refs.basemap["mapObject"];
    mymap.removeLayer(myself.tempOilDivIcon);
    myself.tempOilDivIcon = null;
  }
  get computedTest() {
    return null;
  }

  // TODO:[*] 19-11-12 不再使用此种方式，暂时注释掉
  get current(): Date {
    // TODO:[*] 19-11-07 注意此处的current为string类型（含时区），需要再转换为date
    // return ;

    // let currentStr: string = this.$store.state.current;
    let currentStr: string = this.getcurrent;

    let currentDt: Date = new Date();
    if (currentStr != "") {
      currentDt = new Date(currentStr);
    }
    return currentDt;
  }

  // TODO:[*] 19-11-08 使用vuex-clas的方式监听oil 的两个select
  @Getter("getShowFactor", { namespace: "oil" }) getShowFactor;
  @Watch("getShowFactor")
  OnShowFactor(val: number) {
    console.log(`监听到vuex中namespace:oil factor发生变化:${val}`);
    this.showFactor = val;
    this.loadTrackFactory();
  }

  // TODO:[*] 19-11-12 根据 current showType showFactor决定的加载的layer
  loadTrackFactory(): void {
    let val: number = this.showType;
    // TODO:[*] 19-11-13 加入了clear方法，清除散点以及热图（或放在各个load方法中）
    this.clearAllLayer();
    switch (val) {
      // 散点
      case ShowType.SCATTER:
        // 切换为散点视图
        this.loadTrackScatterPoint();
        break;
      case ShowType.HEATMAP:
        // 切换为热图视图
        this.loadTrackHeatmap();
        break;
    }
  }

  @Getter("getShowType", { namespace: "oil" }) getShowType: number;
  @Watch("getShowType")
  onShowType(val: number) {
    console.log(`监听到vuex中namespace:oil type发生变化:${val}`);
    this.showType = val;
  }

  @Watch("tempOil")
  onOil(oil: OilMidModel) {
    console.log(`监听oil发生变化，现值为${this.tempOil}`);
  }

  @Getter("getCurrent", { namespace: "map" }) getcurrent;
  @Watch("current")
  onCurrent(val: Date) {
    let myself = this;
    this.targetDate = new Date(val);
    // let currentDt: Date = new Date();
    // if (val != "") {
    //   currentDt = new Date(val);
    // }

    // console.log(val);
    // 先加载oil 的realdata，再加载热力图
    this.loadTargetRealData(myself.code, myself.targetDate);
    // TODO:[*] 19-10-31 此处需要加入一个切换的功能
    // this.loadTrackFactory()
    // this.loadTrackHeatmap();
    // TODO:[*] 19-11-12 调用修改后的loadTrack 工厂方法
    this.loadTrackFactory();
  }
}
</script>
<style scoped lang="less">
// TODO:[*] 19-11-13 注意引入less时不需要加.less后缀
@import "../../../styles/base";
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
  }
}
#map_content {
  // 此处放在base.less中的@centermap中
  // padding: 10px;
  flex: 5;
  @centermap();
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
