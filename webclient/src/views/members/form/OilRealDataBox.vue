<template>
  <div class="oil-realdata-box">
    <div class="title">{{realdata.title}}</div>
    <div class="body">
      <div class="main-content">
        <span>{{realdata.main}}</span>
        <span>m/s</span>
      </div>
      <div class="minor-content">
        <span>{{realdata.minor}}</span>
        <span>°</span>
      </div>
    </div>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class OilRealDataBox extends Vue {
  @Prop(Object)
  realdata: { title: string; main: string; minor: string };

  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base";
.oil-realdata-box {
  // background: rgb(54, 15, 144);

  background: linear-gradient(to right, #283958 30%, rgba(4, 107, 114, 0.103));

  display: flex;
  flex-direction: column;
  @allradius();
  @formmoreshadow();
  @formmargin();
  height: 8em;
  .title {
    font-size: 1.8rem;
    font-weight: 500;
    color: white;
    @divshadow();
  }
  .body {
    display: flex;
    height: 100%;
    div {
      display: flex;
      flex: 1;
      align-items: center;
      justify-content: center;
    }
    .main-content {
      font-size: 1.8rem;
      font-weight: 600;
      span:last-of-type {
        font-size: 1.3rem;
        margin-left: 1em;
      }
    }
    .minor-content {
      font-size: 1.4rem;
      span:last-of-type {
        font-size: 1.3rem;
        margin-left: 1em;
      }
      // font-weight: 500;
    }
  }
}
</style>