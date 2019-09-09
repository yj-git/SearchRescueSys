<template>
  <div>
    <l-map ref="basemap" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
    </l-map>
    <TimeBar></TimeBar>
  </div>
</template>
<script lang='ts'>
import L, { LatLng } from "leaflet";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  // 散点数组
  pointList: Array<LatLng> = [];

  // 读取点列表
  loadPointList(): void {}
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
</style>