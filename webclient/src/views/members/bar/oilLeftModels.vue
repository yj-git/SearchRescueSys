<template>
  <div class="oil-model-content">
    <!-- 按照风与流的方式进行拆分 -->
    <OilRealDataBox :realdata="currentRealData()"></OilRealDataBox>
    <OilRealDataBox :realdata="windRealData()"></OilRealDataBox>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import OilRealDataBox from "@/views/members/form/OilRealDataBox.vue";
import { OilMidModel } from "@/middle_model/oil";
@Component({
  components: {
    OilRealDataBox
  }
})
export default class OilLeftModels extends Vue {
  mydata: any = null;

  @Prop(Object)
  oilRealData!: OilMidModel;
  @Prop(String)
  title: string;
  @Watch("realData", { deep: true, immediate: true })
  onRealData(val: any) {
    console.log(val);
  }
  mounted() {}
  get computedTest() {
    return null;
  }

  // TODO:[*] 19-11-21 此处遇见一个问题是若在方法前面加上get会找不到该方法
  currentRealData(): { title: string; main: string; minor: string } {
    let myself = this;
    let realdata: { title: string; main: string; minor: string };
    realdata = {
      title: "流",
      main: myself.oilRealData.currentVal.toString(),
      minor: myself.oilRealData.currentDir.toString()
    };
    return realdata;
  }

  windRealData(): { title: string; main: string; minor: string } {
    let myself = this;
    let realdata: { title: string; main: string; minor: string };
    realdata = {
      title: "风",
      main: myself.oilRealData.windVal.toString(),
      minor: myself.oilRealData.windDir.toString()
    };
    return realdata;
  }
}
</script>
<style scoped lang="less">
.oil-model-content {
  width: 98%;
}
</style>