<template>
    <div>
        <el-table :data="tableData" border style="width: 100%">
            <el-table-column label="日期" width="140">
                <template slot-scope="scope">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 10px">{{ scope.row.date }}</span>
                </template>
            </el-table-column>
            <el-table-column label="作业名" width="140">
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
            <el-table-column label="状态" width="140">
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
            <el-table-column label="用户" width="140">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>用户: {{ scope.row.user }}</p>
                        <!-- <p>住址: {{ scope.row.address }}</p> -->
                        <div slot="reference" class="name-wrapper">
                            <el-tag size="medium">{{ scope.row.user }}</el-tag>
                        </div>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="进度" width="140">
                <template slot-scope="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>进度: {{ scope.row.schedule }}</p>
                        <!-- <p>住址: {{ scope.row.address }}</p> -->
                        <div slot="reference" class="name-wrapper">
                            <el-tag size="medium">{{ scope.row.schedule }}</el-tag>
                        </div>
                    </el-popover>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({})
export default class center_map extends Vue {
    mydata: any = null
    tableData: any = [
        {
            date: '2016-05-02',
            name: 'case_a',
            state: 'running',
            tag: 'doing',
            user: 'xx_1',
            schedule: 80
        }
    ]
    mounted() {}
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
