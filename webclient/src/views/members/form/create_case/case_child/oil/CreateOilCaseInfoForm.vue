<template>
    <div>
        <el-form ref="form" :model="form" label-width="120px" :label-position="labelPosition">
            <el-form-item label="案例名称" :span="8">
                <el-input v-model="form.caseName" :span="6"></el-input>
                <!-- <el-input v-model="form.name" :md="4"></el-input> -->
            </el-form-item>
            <el-form-item label="案例描述">
                <el-input type="textarea" v-model="form.caseDesc"></el-input>
            </el-form-item>
            <el-form-item label="经纬度">
                <el-col :span="11">
                    <el-input v-model="form.lat"></el-input>
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                    <el-input v-model="form.lon"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="时间">
                <el-col :span="11">
                    <el-date-picker
                        type="date"
                        placeholder="选择日期"
                        v-model="form.forecastdate"
                        style="width: 100%;"
                    ></el-date-picker>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="模拟时长">
        <el-input v-model="form.name" size="small"></el-input>
      </el-form-item> -->
            <!-- TODO:[-] 19-11-21 此处修改为计数器的方式 -->
            <el-form-item label="模拟时长">
                <!-- <span class="demonstration">{{ currentNon }}</span> -->
                <el-input-number size="medium" v-model="form.duration"></el-input-number>
            </el-form-item>
            <el-form-item label="失事物类型">
                <el-select placeholder="请选择" v-model="form.goodType">
                    <el-option
                        v-for="item in optionWreckType"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="释放半径">
                <span class="demonstration">{{ form.radius }}</span>
                <el-slider v-model="form.radius"></el-slider>
            </el-form-item>
            <el-form-item label="释放粒子数">
                <span class="demonstration">{{ form.nums }}</span>
                <el-slider v-model="form.nums"></el-slider>
            </el-form-item>
            <!-- <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>-->
        </el-form>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { loadSelectByType } from '@/api/select'
import { SelectTypeEnum } from '@/enum/select'
import { SelectMidModel } from '@/middle_model/select'
import {
    IFormOilCaseInfo,
    IInitSelectFunc,
    loadSelectionByType
} from '@/views/members/form/create_case/case_child/oil/select'
// TODO:[-] 20-02-16 此处放在 ./select.ts中
// export interface IFormOilCaseInfo {
//     caseName: string
//     caseDesc: string
//     lat: number
//     lon: number
//     forecastdate: Date
//     duration: number
//     goodType: number
//     radius: number
//     nums: number
// }
// export interface IInitSelectFunc {
//     (value: string, label: string): void
// }
@Component({})
export default class OilCaseInfoForm extends Vue {
    mydata: any = null
    form: IFormOilCaseInfo = {
        caseName: 'default_case',
        //     caseName='',
        caseDesc: 'default_case',
        lat: 12,
        lon: 12,
        forecastdate: new Date(),
        goodType: 0,
        radius: 0,
        nums: 0,
        duration: 0
        // name: '',
        // region: '',
        // date1: '',
        // date2: '',
        // delivery: false,
        // type: [],
        // resource: '',
        // desc: ''
    }
    // 失事类型
    optionWreckType: Array<{ value: string; label: string }> = [
        {
            value: '0',
            label: 'defalut'
        }
    ]
    // 求解方法
    optionEquationType: Array<{ value: string; label: string }> = [
        {
            value: '0',
            label: 'defalut'
        }
    ]

    labelPosition = 'right'
    burningTime = 72
    radius = 0
    nums = 100
    mounted() {
        // 初始化各个select
        loadSelectionByType(SelectTypeEnum.WRECK, this.initWreckTypeSelect)
        // this.loadSelectByType(SelectTypeEnum.EQUATION, this.initEquationSelect)
    }
    // 提交表达方法
    onSubmit() {}
    // loadSelectByType(type: SelectTypeEnum, func: IInitSelectFunc): void {
    //     this.optionWreckType = []
    //     // const myself = this
    //     loadSelectByType(type).then((res) => {
    //         if (res.status === 200) {
    //             // console.log(res.data)
    //             // 找到所有失事类型的selec集合
    //             if (res.data.length > 0) {
    //                 res.data.map(
    //                     (temp: { name: string; val: string; id: number; type_select: number }) => {
    //                         if (temp.type_select === type) {
    //                             // 此处修改为调用方法
    //                             // this.optionWreckType.push({ value: temp.val, label: temp.name })
    //                             func(temp.val, temp.name)
    //                         }
    //                     }
    //                 )
    //             }
    //         }
    //     })
    // }

    // 初始化 失事类型 select
    initWreckTypeSelect(value: string, label: string): void {
        this.optionWreckType.push({ value: value, label: label })
    }
    // 初始化 求解方法 select
    initEquationSelect(value: string, label: string): void {
        this.optionEquationType.push({ value: value, label: label })
    }

    // get selectType() {
    //     return this.$store.getters['common/productType']
    // }
}
</script>
<style scoped></style>
