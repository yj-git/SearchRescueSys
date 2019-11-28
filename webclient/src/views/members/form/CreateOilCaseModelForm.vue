<template>
  <div>
    <el-form label-width="120px" :label-position="labelPosition">
      <el-form-item label="模拟步长">
        <span class="demonstration">{{ simulationStep }}</span>
        <el-slider v-model="simulationStep"></el-slider>
      </el-form-item>
      <el-form-item label="输出步长">
        <span class="demonstration">{{ consoleStep }}</span>
        <el-slider v-model="consoleStep"></el-slider>
      </el-form-item>
      <el-form-item label="风场不确定性">
        <!-- <span class="demonstration">{{ windNon }}</span> -->
        <el-input-number size="medium" v-model="windNon"></el-input-number>
      </el-form-item>
      <el-form-item label="流场不确定性">
        <!-- <span class="demonstration">{{ currentNon }}</span> -->
        <el-input-number size="medium" v-model="currentNon"></el-input-number>
      </el-form-item>
      <el-form-item label="求解方法">
        <el-select placeholder="请选择" v-model="equation">
          <el-option
            v-for="item in equation"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class OilCaseModelForm extends Vue {
  mydata: any = null;
  simulationStep: number = 10;
  consoleStep: number = 100;
  windNon: number = 4;
  currentNon: number = 2;
  labelPosition: string = "right";
  equation: any = [
    {
      value: "a",
      label: "xx_1"
    }
  ];
  mounted() {}
  // 提交表达方法
  onSubmit() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped></style>
