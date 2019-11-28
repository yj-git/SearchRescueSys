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
          v-for="temp in rescuePointList"
          :key="temp.id"
          :lat-lng="temp.latlon"
        />
        <l-circle
          v-for="temp in rescueScatterPlotList"
          :key="temp.id"
          :lat-lng="temp"
        />
      </l-map>
      <TimeBar
        :targetDate="startDate"
        :days="days"
        :interval="interval"
      ></TimeBar>
    </div>
  </div>
</template>
<script lang="ts">
import * as L from "leaflet";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
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
} from "vue2-leaflet";
import { loadTrackAvgList, loadTrackList } from "@/api/api";
import {
  VectorMidModel,
  RescuePointRealDataMidModel
} from "@/middle_model/rescue";
import TimeBar from "@/views/members/bar/TimeBar.vue";
@Component({
  components: {
    "l-marker": LMarker,
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    "l-polyline": LPolyline,
    "l-circle": LCircle,
    "l-icon": LIcon,
    TimeBar
  }
})
export default class RescueMap extends Vue {
  mydata: any = null;
  code: string = "qz_ty1_100p";
  zoom: number = 5;
  center: any = [17.6, 131.6];
  url: string =
    "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}";

  // 漂移散点
  pointsList: Array<L.LatLng> = [];
  // 搜救漂移点列表
  rescuePointList: Array<RescuePointRealDataMidModel> = [];
  targetDate: Date = new Date();
  // timebar的起始时间
  // startDate: Date = new Date(2016, 6, 22, 3, 0);
  startDate: Date = new Date(2016, 6, 21, 16, 0);
  // TODO:[*] 19-09-10 子组件timebar
  // timebar共有多少天
  days: number = 3;
  // 当前时刻的散点图
  rescueScatterPlotList: Array<number[]> = [];
  interval: number = 24;
  polyline: any = {
    latlngs: [],
    color: "yellow"
  };
  loadTrackAvgList(): void {
    // this.code = "";
    this.clearAll();
    loadTrackAvgList(this.code).then(res => {
      // This condition will always return 'false' since the types 'number' and 'string' have no overlap.
      if (res.status === 200) {
        // res.data.map(vaemp:any=>{

        // })
        res.data.forEach((temp: any) => {
          let tempWind = new VectorMidModel(
            temp["wind"]["x"],
            temp["wind"]["y"]
          );
          let tempCurrent = new VectorMidModel(
            temp["current"]["x"],
            temp["current"]["y"]
          );
          let tempRescue = new RescuePointRealDataMidModel(
            temp.code,
            temp.num,
            // temp.point.coordinates,
            [temp.point.coordinates[1], temp.point.coordinates[0]],
            new Date(temp.time),
            tempCurrent,
            tempWind
          );

          this.rescuePointList.push(tempRescue);
          this.polyline.latlngs.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);
        });
      }
    });
  }
  // 获取指定时刻的散点
  loadTrackScatterPlots(): void {
    // this.clearAll();
    this.clearScatterPlot();
    loadTrackList(this.code, this.targetDate).then(res => {
      if (res.status === 200) {
        res.data.forEach((temp: any) => {
          this.rescueScatterPlotList.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);
        });
      }
    });
  }
  clearAll(): void {
    this.clearCircle();
    this.clearPolyline();
  }
  clearCircle(): void {
    this.rescuePointList = [];
  }
  clearPolyline(): void {
    this.polyline.latlngs = [];
  }
  clearScatterPlot(): void {
    this.rescueScatterPlotList = [];
  }
  mounted() {
    this.loadTrackAvgList();
    // 先给一个当前时间
    this.targetDate = new Date(2016, 6, 21, 16, 0);
    this.startDate = new Date(2016, 6, 21, 16, 0);
    this.loadTrackScatterPlots();
  }
  get computedTest() {
    return null;
  }

  @Getter("getCurrent", { namespace: "map" }) getcurrent;

  get current(): string {
    return this.getcurrent;
  }

  // 监听store中的current
  @Watch("current")
  onCurrent(val: string) {
    // console.log(val);
    this.targetDate = new Date(val);
    this.loadTrackScatterPlots();
    var temp = [];
    // log(val);
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base";
#rescue_map {
  /* height: 100%; */
  // display: flex;
  @center();
  flex-direction: column;
  /* width: 1500px;
  height: 700px; */
  // background: #ff0808;
}
#map_content {
  flex: 1;
  @centermap();
}
</style>
