<template>
  <div id="outliner">
    <h2 :class="numLevelClass">{{ count }}</h2>
    <div>
      <h4>{{ msg }}</h4>
      <a>查看详情 ></a>
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

  mounted() {}
  get computedTest() {
    return null;
  }

  get numLevelClass(): string {
    const primary = 10;
    const info = 20;
    const warning = 50;
    let level = "";
    if (this.count < primary) {
      level = "primary";
    } else if (this.count < info) {
      level = "info";
    } else if (this.count < warning) {
      level = "warning";
    }
    return level;
  }
}
</script>
<style scoped lang="less">
@import "../../../styles/base";
#outliner {
  @allradius();
  display: flex;
  background: rgba(172, 168, 168, 0.924);
  margin: 0.5em;
  padding: 0.75em;
  @formmoreshadow();
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  .primary {
    color: rgb(58, 180, 119);
  }
  .info {
    color: rgb(34, 157, 168);
  }
  .warning {
    color: rgb(206, 76, 25);
  }
  h2 {
    display: flex;
    flex: 1;
    justify-content: center;
    font-size: 300%;
    align-items: center;
  }
  div {
    display: flex;
    flex: 1.5;
    flex-direction: column;
    margin-left: 1em;
    h4 {
      color: rgb(35, 40, 47);
      font-size: 1.25rem;
    }
    a {
      color: rgb(123, 125, 129);
      font-siez: 90%;
    }
  }
}
</style>
