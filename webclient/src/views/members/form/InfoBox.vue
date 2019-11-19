<template>
  <div class="info-box col-md-2" :class="levelstyle">
    <!-- 左侧的icon -->
    <div class="icon"><i class="fa fa-2x" :class="iconstyle"></i></div>
    <!-- 右侧的描述内容 -->
    <div class="content">
      <div class="title">{{ msg }}</div>
      <div class="number">{{ count }}</div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  @Prop(Number)
  count: number;
  @Prop(String)
  msg: string;
  @Prop(String)
  iconstyle: string;
  @Prop(String)
  levelstyle: string;

  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base";
.my-default {
  background-color: #e91e63 !important;
}
.my-info {
  background-color: #00bcd4 !important;
}
.my-succes {
  background-color: #8bc34a !important;
}
.my-warning {
  background-color: #ff9800 !important;
}
.info-box {
  display: flex;
  color: whitesmoke;
  //   background-color: #e91e63 !important;
  padding-left: 0;
  padding-right: 0;
  opacity: 1;
  transition: opacity 2s;
  margin: 1em;
  @formmoreshadow();
  .icon {
    background-color: rgba(0, 0, 0, 0.12);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 1.5em;
  }
  .content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 0.75em;
    .title {
      font-size: 1em;
    }
    .number {
      font-weight: 400;
      font-size: 2em;
    }
  }
}
.info-box:hover {
  background-color: rgba(0, 0, 0, 0.05);
  //   color: transparent;
  //   transition: all 0.95s;
  //   width: 100px;
  opacity: 0.5;
}
</style>
