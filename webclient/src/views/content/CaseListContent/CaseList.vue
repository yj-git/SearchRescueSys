<template>
  <div id="case_list_content">
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column label="日期" width="180">
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span style="margin-left: 10px">{{ scope.row.date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="作业名" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>作业名: {{ scope.row.name }}</p>
            <!-- <p>住址: {{ scope.row.address }}</p> -->
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.name }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>状态: {{ scope.row.state }}</p>
            <!-- <p>住址: {{ scope.row.address }}</p> -->
            <div slot="reference" class="name-wrapper">
              <!-- 通过设置type，设置'primary'为蓝色，'success'为绿色，也可以设置为其他颜色，待试验 -->
              <el-tag
                size="medium"
                :type="scope.row.tag === 'finish' ? 'primary' : 'success'"
              >{{ scope.row.state }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="区域" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>区域: {{ scope.row.area }}</p>
            <!-- <p>住址: {{ scope.row.address }}</p> -->
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.area }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleEdit(scope.$index, scope.row)">加载</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  tableData: any = [
    {
      date: "2016-05-02",
      name: "case_a",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "作业中",
      tag: "doing",
      area:'ind'
    },
    {
      date: "2016-05-04",
      name: "case_b",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "排队中",
      tag: "wait",
      area:'scs'
    },
    {
      date: "2016-05-01",
      name: "case_c",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "已结束",
      tag: "finish",
      area:'bhs'
    },
    {
      date: "2016-05-03",
      name: "case_d",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "排队中",
      tag: "wait",
      area:'ecs'
    }
  ];
  mounted() {}
  get computedTest() {
    return null;
  }
}
</script>
<style scoped>
#case_list_content {
  width: 100%;
}
</style>