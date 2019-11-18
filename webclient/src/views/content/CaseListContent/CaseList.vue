<template>
  <div id="case_list_content">
    <div class="user-statistics">
      <OutLiner :count="35" :msg="'created'"></OutLiner>
      <OutLiner :count="2" :msg="'running'"></OutLiner>
      <OutLiner :count="15" :msg="'completed'"></OutLiner>
      <OutLiner :count="18" :msg="'waiting'"></OutLiner>
    </div>
    <div class="case-statistics">
      <div class="case-listinfo">
        <!-- 左侧的作业列表简况 -->
        <div class="case-list">
          <span>当前作业列表</span>
          <JobCurrent></JobCurrent>
          <!-- <JobProgressbar
            :percent="90"
            :username="'user_1'"
            :casename="'case_xxx_1'"
            :cmt="new Date()"
          ></JobProgressbar>
          <JobProgressbar
            :percent="67"
            :username="'user_1'"
            :casename="'case_xxx_2'"
            :cmt="new Date()"
          ></JobProgressbar>
          <JobProgressbar
            :percent="23"
            :username="'user_1'"
            :casename="'case_xxx_3'"
            :cmt="new Date()"
          ></JobProgressbar>
          <JobProgressbar
            :percent="71"
            :username="'user_1'"
            :casename="'case_xxx_4'"
            :cmt="new Date()"
          ></JobProgressbar> -->
        </div>

        <!-- 用户提交的case的情况
           主要显示最后的case的状态（或所在位置）
       -->
        <div class="user-caseinfo">
          <QueuePercent></QueuePercent>
        </div>
      </div>
      <div class="case-create">
        <div class="create-header">
          <h2>创建case</h2>
          <span>搜集|溢油</span>
        </div>
        <div class="create-body">
          <img src="../../../assets/create_btn.png" />
          <!-- <span>创建搜救或溢油case</span> -->
          <!-- <button>创建作业</button> -->
          <a>创建作业</a>
        </div>
      </div>
    </div>

    <div class="user-content">
      <!-- 按钮区域 -->
      <div class="buttons">
        <el-row>
          <el-button type="primary" icon="el-icon-edit" circle></el-button>
        </el-row>
      </div>
      <div class="my-table">
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
                    >{{ scope.row.state }}</el-tag
                  >
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
              <el-button
                size="mini"
                type="success"
                @click="handleEdit(scope.$index, scope.row)"
                >加载</el-button
              >
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>
      <!-- 加载当前的作业 -->
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
// 引入outliner
import OutLiner from "@/views/members/form/Outliner.vue";
import JobProgressbar from "@/views/members/progress/JobProgressbar.vue";
import JobCurrent from "@/views/members/table/JobCurrent.vue";
import QueuePercent from "@/views/members/percentage/QuenePercent.vue";
@Component({
  components: {
    OutLiner,
    JobProgressbar,
    JobCurrent,
    QueuePercent
  }
})
export default class center_map extends Vue {
  mydata: any = null;
  tableData: any = [
    {
      date: "2016-05-02",
      name: "case_a",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "作业中",
      tag: "doing",
      area: "ind"
    },
    {
      date: "2016-05-04",
      name: "case_b",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "排队中",
      tag: "wait",
      area: "scs"
    },
    {
      date: "2016-05-01",
      name: "case_c",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "已结束",
      tag: "finish",
      area: "bhs"
    },
    {
      date: "2016-05-03",
      name: "case_d",
      address: "上海市普陀区金沙江路 1518 弄",
      state: "排队中",
      tag: "wait",
      area: "ecs"
    }
  ];
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
#case_list_content {
  width: 100%;
  display: flex;
  padding: 0.5em;
  // margin: 0.5em;
  flex-direction: column;
  // 用户的统计信息
  .user-statistics {
    display: flex;
    flex-direction: row;
  }
  // 作业的统计信息
  .case-statistics {
    // height: 500px;
    // background: rgb(189, 123, 123);
    display: flex;
    @margin();
    // flex-direction: row;
    .case-listinfo {
      display: flex;
      flex: 4;
      // height: 400px;
      background: red;
      // flex-direction:
      .case-list {
        background: yellow;
        display: flex;
        flex: 2;
        flex-direction: column;
        margin: 1em;
        @allradius();
        div {
          margin: 1em;
        }
        span {
          display: flex;
          justify-content: flex-start;
          align-items: flex-start;
          margin: 1em;
          color: black;
          font-size: 100%;
        }
        // flex
      }
      .user-caseinfo {
        display: flex;
        background: rgb(146, 146, 69);
        flex: 1;
      }
    }
    // 创建的按钮
    .case-create {
      display: flex;
      flex-direction: column;
      flex: 1;
      height: 400px;
      // background: green;
      // align-items: center;
      justify-content: center;
      .create-header {
        // background-color: #2bbbad !important;
        background: linear-gradient(40deg, #45cafc, #303f9f) !important;
        // @allradius();
        padding: 1.5em;
        box-shadow: 5px 5px 15px #333333;
      }
      .create-body {
        height: 15em;
        // background: blue;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-right: 4%;
        margin-left: 4%;
        box-shadow: 5px 5px 15px #333333;
        // @allradius();
        img {
          height: 8em;
          @margin();
        }
        span {
          @margin();
        }
        button {
          height: 4em;
          width: 4em;
          @allradius();
          @margin();
        }
        // 不再使用bt的btn，改为自己实现的a标签
        a {
          display: inline-block;
          background-color: #880e4f !important;
          padding: 1em;
          border-radius: 0.125rem;
          box-shadow: 5px 5px 15px #333333;
        }
        a:hover {
          box-shadow: 0 5px 11px 0 rgba(0, 0, 0, 0.18),
            0 4px 15px 0 rgba(0, 0, 0, 0.15);
        }
      }
    }
  }
  //
  // 提交的作业列表
  .user-content {
    display: flex;

    flex: 1;
    flex-direction: column;
    // border-bottom-right-radius: 0.5em;
    // border-bottom-left-radius: 0.5em;
    padding-bottom: 1em;
    background: orange;
    @bottomradius();
    // 按钮区
    .buttons {
      display: flex;
      flex: 2;
      background: rgba(119, 119, 219, 0.801);

      .el-row {
        @button();
      }
    }
    // 用户的table
    .my-table {
      display: flex;
      flex: 10;
      background: rgba(107, 197, 197, 0.801);
    }
  }
}
</style>
