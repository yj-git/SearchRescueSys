<template>
    <div>
        <el-form label-width="120px" :label-position="labelPosition">
            <el-form-item label="模拟步长">
                <span class="demonstration">{{ form.simulationStep }}</span>
                <el-slider v-model="simulationStep"></el-slider>
            </el-form-item>
            <el-form-item label="输出步长">
                <span class="demonstration">{{ form.consoleStep }}</span>
                <el-slider v-model="consoleStep"></el-slider>
            </el-form-item>
            <el-form-item label="风场不确定性">
                <!-- <span class="demonstration">{{ windNon }}</span> -->
                <el-input-number size="medium" v-model="form.windNon"></el-input-number>
            </el-form-item>
            <el-form-item label="流场不确定性">
                <!-- <span class="demonstration">{{ currentNon }}</span> -->
                <el-input-number size="medium" v-model="form.currentNon"></el-input-number>
            </el-form-item>
            <el-form-item label="求解方法">
                <el-select placeholder="请选择" v-model="form.equation">
                    <el-option
                        v-for="item in optionEquationType"
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
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { SelectTypeEnum } from '@/enum/select'
import {
    IFormOilCaseInfo,
    IFormOilCaseModel,
    IInitSelectFunc,
    loadSelectionByType
} from '@/views/members/form/create_case/case_child/oil/select'
@Component({})
export default class OilCaseModelForm extends Vue {
    mydata: any = null
    simulationStep = 10
    consoleStep = 100
    windNon = 4
    currentNon = 2
    labelPosition = 'right'
    equation: any = [
        {
            value: 'a',
            label: 'xx_1'
        }
    ]
    form: IFormOilCaseModel = {
        simulationStep: 0,
        consoleStep: 0,
        windNon: 0,
        currentNon: 0,
        optionEquationType: 0
    }
    // 求解方法
    optionEquationType: Array<{ value: string; label: string }> = [
        {
            value: '0',
            label: 'defalut'
        }
    ]
    mounted() {
        loadSelectionByType(SelectTypeEnum.EQUATION, this.initEquationSelect)
    }
    // 初始化 求解方法 select
    initEquationSelect(value: string, label: string): void {
        this.optionEquationType.push({ value: value, label: label })
    }
    // 提交表达方法
    onSubmit() {}
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
