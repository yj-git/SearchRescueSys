<template>
    <div>
        <div class="card mt10">
            <div class="card-header card-my-header">
                多条件搜索
            </div>
            <form class="card-body card-my-body">
                <div class="form-row">
                    <div class="form-group col-md-6 form-inline">
                        <div class="col-sm-3 smdiv">
                            <label for="inputEmail4">类别</label>
                        </div>
                        <!-- <input v-model="level" class="form-control col-md-7" /> -->
                        <!-- <select class="from-control col-md-7" v-model="coverageType">
                            <option
                                v-for="item in coverageTypes"
                                :key="item.key"
                                :value="item.key"
                                >{{ item.name }}</option
                            >
                        </select> -->
                        <el-select v-model="coverageArea" placeholder="请选择" @change="setType">
                            <el-option
                                v-for="item in coverageAreas"
                                :key="item.key"
                                :label="item.name"
                                :value="item.key"
                            ></el-option>
                        </el-select>
                    </div>
                    <div class="form-group col-md-6 form-inline">
                        <div class="col-sm-3 smdiv">
                            <label for="inputEmail4">区域</label>
                        </div>
                        <!-- <input v-model="level" class="form-control col-md-7" /> -->
                        <!-- <select class="from-control col-md-7" v-model="coverageArea">
                            <option
                                v-for="item in coverageAreas"
                                :key="item.key"
                                :value="item.key"
                                >{{ item.name }}</option
                            >
                        </select> -->
                        <el-select v-model="coverageArea" placeholder="请选择" @change="setType">
                            <el-option
                                v-for="item in coverageAreas"
                                :key="item.key"
                                :label="item.name"
                                :value="item.key"
                            ></el-option>
                        </el-select>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group col-md-6 form-inline" style="text-align:left;">
                        <div class="col-sm-3 smdiv">
                            <label>起始月</label>
                        </div>

                        <el-date-picker
                            v-model="startMonth"
                            type="month"
                            placeholder="起始月"
                            style="width:60%;"
                        ></el-date-picker>
                    </div>
                </div>
                <el-button type="primary" icon="el-icon-search" @click="loadSearchResult"
                    >搜索</el-button
                >
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'

// 历史栅格数据查询列表
export default class CoverageSearchForm extends Vue {
    coverageType = 0
    coverageArea = 0
    coverageTypes: Array<{ key: number; name: string }> = []
    coverageAreas: Array<{ key: number; name: string }> = []
}
</script>

<style lang="less" scoped>
.card {
    background-color: transparent !important;
    /* 对于多条件搜索的card的一些样式 */
    .card-my-header {
        background: linear-gradient(to right, #1a6865 30%, rgba(4, 107, 114, 0.639));
        font-size: 90%;
        text-shadow: 2px 2px 8px rgb(33, 32, 32);
        width: 100%;
    }
    /* 自动以的card-body样式 */
    .card-my-body {
        background: linear-gradient(to right, #248e8a 30%, rgba(4, 107, 114, 0.639));
        padding: 8px 8px 8px 8px;
        width: 100%;
        .form-row {
            .form-group {
                display: flex;
                .smdiv {
                    display: flex;
                    max-width: 40%;
                    flex: 4;
                }
                .el-select {
                    display: flex;
                    flex: 6;
                    max-width: 60%;
                }
            }
        }
    }
    .btn-my {
        background: #2988d2;
    }
}
#data_list {
    margin-top: 5px;
    background: rgba(73, 115, 165, 0.701);
    padding-right: 8px;
    border-radius: 5px;
}
li {
    list-style: none;
    text-align: left;
}

.list-my-group-item {
    color: rgb(4, 4, 4);
    font-size: 85%;
    background: rgba(184, 206, 200, 0.557);
    padding-top: 5px;
    padding-bottom: 5px;
    font-weight: 400;
    text-shadow: 2px 2px 8px rgb(33, 32, 32);
}

.list-my-group-item:hover {
    color: rgb(255, 255, 255);
    font-size: 85%;
    background: rgba(111, 238, 204, 0.557);
    padding-top: 5px;
    padding-bottom: 5px;
    font-weight: 600;
}
.form-group .control-label {
    color: #ffffff;
    font-family: 'Lato', Helvetica, Arial, sans-serif;
}

#job-list {
    margin-top: 5px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
    /* 0.5s动画过渡的时间 */
}
.fade-enter,
.fade-leave-to {
    opacity: 0;
}

/* 自动以的card-body样式 */
#my_condition .card-my-body {
    /* background: linear-gradient(to right, #248e8a 30%, rgba(4, 107, 114, 0.639)); */
    padding-left: 24px;
}
</style>
