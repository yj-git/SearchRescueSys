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
                        <el-select v-model="coverageType" placeholder="请选择" @change="setType">
                            <el-option
                                v-for="item in coverageTypes"
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
                        <el-select v-model="coverageArea" placeholder="请选择">
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
                            <label>选定日期</label>
                        </div>

                        <el-date-picker
                            v-model="selectCurrent"
                            type="date"
                            placeholder="选定日期"
                            style="width:60%;"
                        ></el-date-picker>
                    </div>
                </div>
                <el-button type="primary" icon="el-icon-search" @click="submitCoverageCondition"
                    >搜索</el-button
                >
            </form>
        </div>
        <transition name="fade">
            <div class="card mt10">
                <div class="card-header card-my-header">
                    栅格数据列表
                </div>
                <div class="card-header card-my-body">
                    <div class="row">
                        <div class="col">
                            <!-- 暂时不使用之前的 ul -> li 的方式 -->
                            <!-- <ul class="list-group">
                                <li
                                    class="list-group-item"
                                    v-for="(item, index) in coverageList"
                                    :key="index"
                                    @click="loadCoverageInfo(item)"
                                >
                                    {{ item.name }}
                                </li>
                            </ul> -->
                            <table class="table">
                                <thead class="thead-dark">
                                    <tr>
                                        <th scope="col">id</th>
                                        <th scope="col">文件名</th>
                                        <th scope="col">区域</th>
                                        <th scope="col">类型</th>
                                        <th scope="col">文件大小</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="(item, index) in coverageList"
                                        :key="index"
                                        @click="selectCoverage(item)"
                                    >
                                        <th scope="row">{{ item.key }}</th>
                                        <td>{{ item.name }}</td>
                                        <td>{{ item.areaId }}</td>
                                        <td>{{ item.typeId }}</td>
                                        <td>{{ item.size }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { loadSelectByType, loadSelectParentByType } from '@/api/select'
import { loadCoverageList } from '@/api/geo'
import { SelectTypeEnum } from '@/enum/select'
import { DictEnum } from '@/enum/dict'
import { DEFAULT_SELECT_KEY, DEFAULT_SELECT_ITEM, DEFAULT_DICT_KEY } from '@/const/common'
import { Mutation, State, namespace } from 'vuex-class'
// vuex -> types
import { SET_GEO_COVERAGEID } from '@/store/types'
// 历史栅格数据查询列表
@Component({})
export default class CoverageSearchForm extends Vue {
    coverageType = DEFAULT_SELECT_KEY
    dictType = DEFAULT_DICT_KEY
    coverageArea = DEFAULT_SELECT_KEY
    dictArea = DEFAULT_DICT_KEY
    selectCurrent: Date = new Date()
    coverageTypes: { key: number; name: string; did: number }[] = [DEFAULT_SELECT_ITEM]
    coverageAreas: { key: number; name: string; did: number }[] = [DEFAULT_SELECT_ITEM]
    coverageList: {
        key: number
        name: string
        areaId: number
        typeId: number
        size: number
    }[] = []
    mounted(): void {
        loadSelectParentByType(DictEnum.COVERAGE_TYPE).then(
            (res: {
                data: { menu_titl: string; id: number; menu_content: string; did_id: number }[]
                status: number
            }) => {
                if (res.status == 200) {
                    // console.log(res.data)
                    if (res.data.length > 0) {
                        res.data.forEach((temp) => {
                            this.coverageTypes.push({
                                key: temp.id,
                                name: temp.menu_content,
                                did: temp.did_id
                            })
                        })
                    }
                }
            }
        )
    }
    created(): void {
        // console.log('加载完成')
    }
    setType(key: number): void {
        this.coverageType = key
    }
    selectCoverage(val: {
        key: number
        name: string
        areaId: number
        typeId: number
        size: number
    }): void {
        console.log(val)
        this.selectCoverageId(val.key)
        // this.$store
        //     .dispatch('geo/setCoverageID', val.key)
        //     .then(() => {
        //         console.log(`CoverageSearchForm存入->geo/coverageId:${val.key}`)
        //     })
        //     .catch((err) => {
        //         console.log(`出现错误:${err}`)
        //     })
    }

    /*
        TODO:[-] 20-04-16 
        No overload matches this call.
        Overload 1 of 2, '(proto: Vue, key: string): void', gave the following error.
        Argument of type '"SET_GEO_COVERAGEID"' is not assignable to parameter of type 'Vue'.
        Overload 2 of 2, '(type: string, options?: BindingOptions | undefined): VuexDecorator', gave the following error.
        Argument of type '{ name: string; }' is not assignable to parameter of type 'BindingOptions'.
        Object literal may only specify known properties, and 'name' does not exist in type 'BindingOptions'.
    */
    @Mutation(SET_GEO_COVERAGEID, { namespace: 'geo' }) selectCoverageId

    submitCoverageCondition(): void {
        console.log(
            `type:${this.coverageType}-dict:${this.dictType}|area:${this.coverageArea}-dict:${this.dictArea}|current:${this.selectCurrent}`
        )
        if (this.coverageArea === DEFAULT_SELECT_KEY || this.coverageType === DEFAULT_SELECT_KEY) {
            console.log('有未选择的选项')
        }
        loadCoverageList(this.dictType, this.dictArea, this.selectCurrent).then((res) => {
            if (res.status === 200) {
                this.coverageList = []
                if (res.data.length > 0) {
                    res.data.forEach((temp) => {
                        this.coverageList.push({
                            key: temp.id,
                            name: temp.file_name,
                            areaId: temp.coverage_area,
                            typeId: temp.coverage_type,
                            size: temp.file_size
                        })
                    })
                }
                // console.log(res.data)
            }
        })

        // 将 area|type|current 作为参数 -> django
    }
    loadCoverageInfo(): void {}

    @Watch('coverageArea')
    onCoverageArea(key: number): void {
        const tempArea = this.coverageAreas.find((temp) => temp.key === key)
        if (tempArea != undefined) this.dictArea = tempArea.did
    }

    @Watch('coverageType')
    onCoverageType(key: number): void {
        // console.log(key)
        // TODO:[-] 20-04-15 监听 type 变化后 -> 修改 对应的字典
        const tempType = this.coverageTypes.find((temp) => temp.key === key)
        if (tempType != undefined) this.dictType = tempType.did

        loadSelectByType(SelectTypeEnum.COVERAGE_AREA, key).then(
            (res: {
                data: { menu_titl: string; id: number; menu_content: string; did_id: number }[]
                status: number
            }) => {
                if (res.status == 200) {
                    if (res.data.length > 0) {
                        // console.log(res.data)
                        // 注意先清空
                        this.coverageAreas = []
                        res.data.forEach((temp) => {
                            this.coverageAreas.push({
                                key: temp.id,
                                name: temp.menu_content,
                                did: temp.did_id
                            })
                        })
                    }
                }
            }
        )
    }
}
</script>

<style lang="less" scoped>
.card {
    background-color: transparent !important;
    // 新加一个每个card的底部空余
    margin-bottom: 1rem;
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
