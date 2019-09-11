<template>
  <div id="left_bar">
    <el-row class="tac">
      <el-col :span="24">
        <h5></h5>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>风流数据</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="1-1">
                <router-link to="/caselist">历史案例</router-link>
              </el-menu-item>
              <el-menu-item index="1-2">
                <router-link to="/windmap">风场数据</router-link>
              </el-menu-item>
              <el-menu-item index="1-3">
                <router-link to="/currentmap">流场数据</router-link>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>搜救结果</span>
            </template>
            <el-menu-item-group>
              <template slot="title">案例查询</template>
              <el-menu-item index="1-2">
                <router-link to="/rescuemap">历史案例</router-link>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>溢油结果</span>
            </template>
            <el-menu-item-group>
              <template slot="title">案例查询</template>
              <el-menu-item index="1-1">条件搜索</el-menu-item>
              <el-menu-item index="1-2">历史结果列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-col>
    </el-row>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#left_bar {
  display: flex;
  /* flex: 3; */
  width: 200px;
  /* height: 100%; */
  background: #4dac8cd3;
}
</style>