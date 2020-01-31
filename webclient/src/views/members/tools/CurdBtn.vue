<template>
  <div>
    <div class="user-statistics">
      <!-- <OutLiner :count="35" :msg="'created'"></OutLiner>
      <OutLiner :count="2" :msg="'running'"></OutLiner>
      <OutLiner :count="15" :msg="'completed'"></OutLiner>
      <OutLiner :count="18" :msg="'waiting'"></OutLiner>-->
      <!-- TODO:[-] 19-11-19 注意此处对组件直接通过@click绑定是无效的，需要通过@click.native进行绑定click事件 -->
      <InfoBox
        :msg="'创建case'"
        :iconstyle="'fa-edit'"
        :levelstyle="'my-default'"
        :showsize="'small'"
      ></InfoBox>
      <!-- <InfoBox
        :count="2"
        :msg="'running'"
        :iconstyle="'fa-refresh fa-spin'"
        :levelstyle="'my-info'"
      ></InfoBox> -->
      <InfoBox
        :msg="'历史查询'"
        :iconstyle="'fa-stop-circle'"
        :levelstyle="'my-succes'"
        :showsize="'small'"
      ></InfoBox>
      <!-- <InfoBox
        :count="18"
        :msg="'waiting'"
        :iconstyle="'fa-pause-circle'"
        :levelstyle="'my-warning'"
      ></InfoBox> -->
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import InfoBox from "@/views/members/form/InfoBox.vue";
@Component({
  components: { InfoBox }
})
export default class CurdBtn extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base.less";
@margin: {
  margin: 0.5em;
};
.user-statistics {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#case_list_content {
  width: 100%;
  display: flex;
  padding: 0.5em;
  // margin: 0.5em;
  flex-direction: column;
  @centerbackground();
  // 用户的统计信息
}
</style>
