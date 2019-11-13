<template>
  <div id="oil_factor_select">
    <!-- <h1>模式切换</h1> -->
    <div class="show">
      <div class="row">
        <span>显示模式</span>
        <el-select
          v-model="valueShowTypes"
          placeholder="请选择"
          @change="setType"
        >
          <el-option
            v-for="item in optionsShowTypes"
            :key="item.key"
            :label="item.label"
            :value="item.key"
          ></el-option>
        </el-select>
      </div>
      <div class="row">
        <span>权重</span>
        <el-select
          v-model="valueFactors"
          placeholder="请选择"
          @change="setFactor"
        >
          <el-option
            v-for="item in optionsFactors"
            :key="item.key"
            :label="item.label"
            :value="item.key"
          ></el-option>
        </el-select>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { mapMutations } from "vuex";
import { Mutation, namespace } from "vuex-class";

// const oilModule = namespace("oilStore");

// 引入常量
import { optionsFactors, optionsShowTypes } from "@/const/Oil";

@Component({})
export default class OilFactorSelect extends Vue {
  optionsFactors: { value: string; label: string; key: number }[] = [];
  // 默认值
  valueFactors = 0;
  optionsShowTypes: { value: string; label: string; key: number }[] = [];
  valueShowTypes = 0;

  // TODO:[*] 19-11-08
  /* error：
  [vuex] unknown mutation type: setShowFactor
  */
  // @oilModule.Mutation("setShowFactor") mutationShowFactor;
  @Mutation("setShowFactor", { namespace: "oil" }) setShowFactor;
  // @Mutation setShowFactor: any;

  @Mutation("setShowType", { namespace: "oil" }) setShowType;

  mounted() {
    let myself = this;
    console.log("select 加载成功");
    this.optionsFactors = optionsFactors;
    // this.mutationShowFactor({ data: myself.optionsFactors });
    this.optionsShowTypes = optionsShowTypes;
    this.setType(this.valueShowTypes);
    this.setFactor(this.valueFactors);
  }

  setType(val: number): void {
    console.log(`选中显示模式${val}`);
    this.setShowType({ data: val });
  }

  setFactor(val: number): void {
    console.log(`选中权重${val}`);
    this.setShowFactor({ data: val });
  }
  // ...mapMutations(['getShowFactor','getShowType'])
  get computedTest() {
    return null;
  }
}
</script>
<style lang="less" scoped>
#oil_factor_select {
  display: flex;
  flex-direction: column;
}

#oil_factor_select .show {
  .show {
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 2;
    width: 30%;
    background: #99a9bf;
  }
}
.row {
  //   background: #d3dce6;
  /* margin-bottom: 20px; */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 30px;
}
.el-select {
  width: 60%;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
