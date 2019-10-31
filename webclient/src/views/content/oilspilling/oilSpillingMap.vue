<template>
  <div id="rescue_map">
    <div id="map_content">
      <l-map ref="basemap" :zoom="zoom" :center="center">
        <l-tile-layer :url="url"></l-tile-layer>
        <l-polyline :lat-lngs="polyline.latlngs" :fill="false" :color="polyline.color"></l-polyline>

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
    </div>
    <div id="right_bar">
      <!-- TODO:[*] 19-10-28 加入右侧信息栏_v1版本 -->
      <!-- <RightOilBar></RightOilBar> -->
      <OilRightBar :oilRealData="oilAvgRealData"></OilRightBar>
    </div>
    <!-- <RightDetailBar :oil="tempOil"></RightDetailBar> -->
    <!-- <RightDetailBar :oil="tempOil"></RightDetailBar> -->
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import * as L from "leaflet";
// TODO:[*] 19-10-16 加入vue2 leaflet heatmap不使用以下的方式
// import { HeatmapOverlay } from "heatmap.js";

import { Getter, Mutation, State } from "vuex-class";
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
import {
  loadOilSpillingAvgTrackList,
  loadOilScatterTrackList,
  loadOilRealData,
  loadOilSpillingAvgRealData
} from "@/api/api";

import { OilPointRealDataMidModel } from "@/middle_model/rescue";
import { OilMidModel } from "@/middle_model/oil";
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
    OilRightBar
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
  targetDate: Date;
  // 溢油平均轨迹
  oilAvgPointList: Array<OilPointRealDataMidModel> = [];
  // TODO:[*] 19-10-31 由于设置类型为any，且赋值为null，引发的子组件在为null的情况下未渲染
  oilAvgRealData: any = null;
  // 指定时刻的全部轨迹散点数组
  oilScatterPointList: Array<number[]> = [];
  oilScatterCircleList: Array<any> = [];
  oilHeatmapList: Array<any> = [];
  polyline: any = {
    latlngs: [],
    color: "yellow"
  };
  // timebar的起始时间
  startDate: Date = new Date(2018, 0, 14, 22, 20);
  interval: number = 24;
  // timebar共有多少天
  days: number = 3;
  tempOilDivIcon: any = null;
  tempOil: any = null;
  mounted() {
    // 由于是测试，页面加载完成后先加载当前 code 的平均轨迹
    this.loadTrackAvgList();
    this.startDate = new Date(2018, 0, 14, 22, 20);
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
  loadTrackScatterPlots(): void {
    this.clearScatterPoint();
    let mymap: any = this.$refs.basemap["mapObject"];
    this.oilHeatmapList = [];
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
        heatLayer.addTo(mymap);
      }
    });
  }

  clearScatterPoint(): void {
    let mymap: any = this.$refs.basemap["mapObject"];
    this.oilScatterPointList = [];
    this.oilScatterCircleList.forEach(temp => {
      mymap.removeLayer(temp);
    });
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

  get current(): string {
    return this.$store.state.current;
  }

  @Watch("tempOil")
  onOil(oil: OilMidModel) {
    console.log(`监听oil发生变化，现值为${this.tempOil}`);
  }

  @Watch("current")
  onCurrent(val: string) {
    let myself = this;
    this.targetDate = new Date(val);

    // console.log(val);
    // 先加载oil 的realdata，再加载热力图
    this.loadTargetRealData(myself.code, myself.targetDate);
    // TODO:[*] 19-10-31 此处需要加入一个切换的功能
    this.loadTrackScatterPlots();

    // this
  }
}
</script>
<style>
#rescue_map {
  /* height: 100%; */
  /* display: flex;
  flex-direction: column; */
  display: flex;
  /* flex-direction: column; */
  flex: 22;
  /* width: 1500px;
  height: 700px; */
  /* background: #2a79d4; */
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));
}
#map_content {
  padding: 10px;
  flex: 5;
}
#right_bar {
  flex: 1;
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