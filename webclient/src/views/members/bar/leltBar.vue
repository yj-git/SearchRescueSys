<template>
  <div id="left_bar">
    <!-- <el-row class="tac">
      <el-col :span="24">
        <h5></h5>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#4dac8cd3"
          text-color="rgba(5, 71, 116, 0.829)"
          active-text-color="#ffd04b"
          mode="horizontal"
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
              
              <el-menu-item index="1-2">
                <router-link to="/oilmap">历史案例</router-link>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-col>
    </el-row>-->
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#283958"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <!-- 作业列表 -->
      <el-submenu index="1">
        <template slot="title"
          >作业列表</template
        >
        <el-menu-item index="2-1">
          <router-link to="/caselist">历史案例</router-link>
        </el-menu-item>
      </el-submenu>
      <!-- 风场及流场 -->
      <el-submenu index="2">
        <template slot="title"
          >风场及流场</template
        >
        <el-menu-item index="2-1">
          <router-link to="/caselist">风场</router-link>
        </el-menu-item>
        <el-menu-item index="2-2">
          <router-link to="/windmap">流场</router-link>
        </el-menu-item>
      </el-submenu>
      <!-- 搜救模型 -->
      <el-submenu index="3">
        <template slot="title"
          >搜救</template
        >
        <el-menu-item index="2-1">
          <router-link to="/rescuemap">历史案例</router-link>
        </el-menu-item>
      </el-submenu>
      <!-- 溢油模型 -->
      <el-submenu index="4">
        <template slot="title"
          >溢油</template
        >
        <el-menu-item index="4-1">
          <router-link to="/oilmap">展示方式1</router-link>
        </el-menu-item>
        <el-menu-item index="4-2">
          <router-link to="/newoilmap">展示方式2</router-link>
        </el-menu-item>
        <el-menu-item index="4-3">
          <router-link to="/mergeoilmap">展示方式3</router-link>
        </el-menu-item>
      </el-submenu>
    </el-menu>
    <!-- <div class="line"></div> -->
  </div>
</template>
<script lang="ts">
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
<style scoped lang="less">
#left_bar {
  display: flex;
  flex-direction: column;
  .el-menu--horizontal {
    // background: #115368ef;
    // 去掉element ui 导航栏的底部的bottom的dash边框
    border-bottom: 0px;
  }
}
</style>
