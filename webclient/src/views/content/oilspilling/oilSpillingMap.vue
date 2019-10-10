<template>
  <div id="rescue_map">
    <l-map ref="basemap" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-polyline :lat-lngs="polyline.latlngs" :fill="false" :color="polyline.color"></l-polyline>

      <l-circle
        v-for="temp in oilAvgPointList"
        :key="temp.id"
        :lat-lng="temp.latlon"
        @click="testOnOver(temp)"
      />
      <!-- <l-circle v-for="temp in oilScatterPointList" :key="temp.id" :lat-lng="temp" /> -->
    </l-map>
    <TimeBar :targetDate="startDate" :days="days" :interval="interval"></TimeBar>
    <!-- <RightDetailBar :oil="tempOil"></RightDetailBar> -->
    <RightDetailBar :oil="tempOil"></RightDetailBar>
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
import RightDetailBar from "@/views/members/bar/rightBarDetail.vue";
import {
  loadOilSpillingAvgTrackList,
  loadOilScatterTrackList,
  loadOilRealData
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
    RightDetailBar
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
  // 指定时刻的全部轨迹散点数组
  oilScatterPointList: Array<number[]> = [];
  oilScatterCircleList: Array<any> = [];
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
    loadOilScatterTrackList(this.code, this.targetDate).then(res => {
      if (res.status === 200) {
        // TODO : [*] 19-09-25 注意此处 使用leaflet2vue插件会导致vue的组件崩溃。
        // 尝试使用直接添加的方式
        res.data.forEach((temp: any) => {
          this.oilScatterPointList.push([
            temp.point.coordinates[1],
            temp.point.coordinates[0]
          ]);
          let temp_circle = L.circle(
            [temp.point.coordinates[1], temp.point.coordinates[0]],
            {
              radius: 30
            }
          ).addTo(mymap);
          this.oilScatterCircleList.push(temp_circle);
        });
        // 获取到当前的map
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
    this.targetDate = new Date(val);
    // console.log(val);
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
  width: 1500px;
  height: 700px;
  background: #ff0808;
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