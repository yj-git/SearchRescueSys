<template>
    <div id="job-list">
        <!-- 按钮区域 -->
        <!-- <div class="buttons">
      <el-row>
        <el-button type="primary" icon="el-icon-edit" circle></el-button>
      </el-row>
    </div>-->
        <div class="my-table">
            <el-table
                :data="tableData"
                border
                style="width: 100%"
                :row-style="rowStyle"
                :header-cell-style="rowStyle"
            >
                <el-table-column label="日期" width="180">
                    <template slot-scope="scope">
                        <i class="el-icon-time"></i>
                        <span style="margin-left: 10px">{{ scope.row.date }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="作业名" width="columnWidth">
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
                <el-table-column label="状态" width="columnWidth">
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
                <el-table-column label="区域" width="columnWidth">
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
                <el-table-column label="操作" width="180" v-if="!isMin">
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
                <el-table-column label="状态" width="180" v-if="!isMin">
                    <template slot-scope="scope">
                        <el-progress
                            :text-inside="true"
                            :stroke-width="26"
                            :percentage="scope.row.percent"
                            :status="getStatusLevel(scope.row.percent)"
                        ></el-progress>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 加载当前的作业 -->
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({
    filters: {
        getStatusLevel(val: number) {}
    }
})
export default class JobListUser extends Vue {
    mydata: any = null
    tableData: any = [
        {
            date: '2016-05-02',
            name: 'case_a',
            address: '上海市普陀区金沙江路 1518 弄',
            state: '作业中',
            tag: 'doing',
            area: 'ind',
            percent: 56
        },
        {
            date: '2016-05-04',
            name: 'case_b',
            address: '上海市普陀区金沙江路 1518 弄',
            state: '排队中',
            tag: 'wait',
            area: 'scs',
            percent: 0
        },
        {
            date: '2016-05-01',
            name: 'case_c',
            address: '上海市普陀区金沙江路 1518 弄',
            state: '已结束',
            tag: 'finish',
            area: 'bhs',
            percent: 100
        },
        {
            date: '2016-05-03',
            name: 'case_d',
            address: '上海市普陀区金沙江路 1518 弄',
            state: '作业中',
            tag: 'doing',
            area: 'ecs',
            percent: 42
        }
    ]
    mounted() {}
    getStatusLevel(val: number): string {
        let level = ''
        if (val < 50) {
            level = 'exception'
        } else if (val < 80) {
            level = 'warning'
        } else if (val >= 80) {
            level = 'success'
        }
        return level
    }
    // 是否为缩小版
    @Prop({ default: false })
    isMin!: boolean

    get computedTest() {
        return null
    }
    get columnWidth() {
        return this.isMin ? 120 : 180
    }

    get rowStyle(): string {
        let style = ''
        if (this.isMin) {
            style = 'background-color:#329d96;color: #fff;font-weight: 500;'
        }
        return style
    }
}
</script>
<style lang="less">
@import '../../../styles/base.less';
// 提交的作业列表
#job-list {
    display: flex;
    // @formmoreshadow();
    flex: 1;
    flex-direction: column;
    align-items: center;
    // border-bottom-right-radius: 0.5em;
    // border-bottom-left-radius: 0.5em;
    //   padding-bottom: 1em;
    // background: orange;
    // width: 70%;
    //   margin: 1em;
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
        width: 70%;
        @formmoreshadow();
    }
}
// 修改elementui自定义的table样式
.el-table--border td {
    border-right: none;
    // display: flex;
}
.el-table td {
    border-bottom: none;
}
.el-table th.is-leaf {
    border: none;
}
</style>
