<template>
    <div>
        <el-form ref="form" :model="form" label-width="120px" :label-position="labelPosition">
            <el-form-item label="案例名称" :span="8">
                <el-input v-model="form.name" :span="6"></el-input>
                <!-- <el-input v-model="form.name" :md="4"></el-input> -->
            </el-form-item>
            <el-form-item label="案例描述">
                <el-input type="textarea" v-model="form.desc"></el-input>
            </el-form-item>
            <el-form-item label="经纬度">
                <el-col :span="11">
                    <el-input v-model="form.name"></el-input>
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                    <el-input v-model="form.name"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="时间">
                <el-col :span="11">
                    <el-date-picker
                        type="date"
                        placeholder="选择日期"
                        v-model="form.date1"
                        style="width: 100%;"
                    ></el-date-picker>
                </el-col>
            </el-form-item>
            <el-form-item label="模拟时长">
                <el-input v-model="form.name" size="small"></el-input>
            </el-form-item>
            <el-form-item label="失事物类型">
                <el-select placeholder="请选择">
                    <el-option
                        v-for="item in optionWreckType"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="释放半径">
                <span class="demonstration">{{ radius }}</span>
                <el-slider v-model="radius"></el-slider>
            </el-form-item>
            <el-form-item label="释放粒子数">
                <span class="demonstration">{{ nums }}</span>
                <el-slider v-model="nums"></el-slider>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">立即创建</el-button>
                <el-button>取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
@Component({})
export default class CreatedRescueCaseForm extends Vue {
    mydata: any = null
    form: any = {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
    }
    // 失事类型
    optionWreckType: any = [
        {
            value: 'a',
            label: 'xx_1'
        }
    ]
    labelPosition = 'right'
    radius = 0
    nums = 100
    mounted() {}
    // 提交表达方法
    onSubmit() {}
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
