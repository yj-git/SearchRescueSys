<template>
  <div id="rescue_map">
    <l-map ref="basemap" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <!-- <l-polyline :lat-lngs="polyline.latlngs" :fill="false" :color="polyline.color"></l-polyline> -->

      <l-circle v-for="temp in oilAvgPointList" :key="temp.id" :lat-lng="temp.latlon" />
      <!-- <l-circle v-for="temp in rescueScatterPlotList" :key="temp.id" :lat-lng="temp" />-->
    </l-map>
    <TimeBar :targetDate="startDate" :days="days" :interval="interval"></TimeBar>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import * as L from "leaflet";
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
} from "vue2-leaflet";

import TimeBar from "@/views/members/bar/TimeBar.vue";
import { loadOilSpillingAvgTrackList } from "@/api/api";

import { OilPointRealDataMidModel } from "@/middle_model/rescue";
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
export default class center_map extends Vue {
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
  mounted() {
    // 由于是测试，页面加载完成后先加载当前 code 的平均轨迹
    this.loadTrackAvgList();
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
        });
      }
      console.log(res.data);
    });
  }
  get computedTest() {
    return null;
  }

  get current(): string {
    return this.$store.state.current;
  }

  @Watch("current")
  onCurrent(val: string) {
    this.targetDate = new Date(val);
    // this
  }
}
</script>
<style scoped>
#rescue_map {
  /* height: 100%; */
  /* display: flex;
  flex-direction: column; */
  width: 1500px;
  height: 700px;
  background: #ff0808;
}
</style>    