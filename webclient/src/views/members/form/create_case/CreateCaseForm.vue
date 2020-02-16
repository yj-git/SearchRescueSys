<template>
    <div>
        <el-tabs v-model="activeTemp" @tab-click="handleClick">
            <el-tab-pane label="搜救case" name="first">
                <CreateRescueCaseForm></CreateRescueCaseForm>
                <!-- <el-tabs :tab-position="childTablPosition">
                    <el-tab-pane label="搜救信息参数">
                        <OilCaseInfoForm></OilCaseInfoForm>
                    </el-tab-pane>
                </el-tabs> -->
            </el-tab-pane>
            <el-tab-pane label="溢油case" name="second">
                <!-- TODO:[*] 19-11-21 加入了左侧的tab，右侧放现在的溢油的form表单 -->
                <!-- 左侧的tab包含 
        [x] 1- 搜救信息参数
        [ ] 2- 模型参数-->
                <!-- <el-tabs :tab-position="childTablPosition">
                    <el-tab-pane label="搜救信息参数">
                        <OilCaseInfoForm></OilCaseInfoForm>
                    </el-tab-pane>
                    <el-tab-pane label="模型参数">
                        <OilCaseModelForm></OilCaseModelForm>
                    </el-tab-pane>
                </el-tabs> -->
                <CreateOilCaseForm ref="oil"></CreateOilCaseForm>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
// import CreateOilCase from '@/views/members/form/CreateOilCaseForm.vue'
import OilCaseInfoForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseInfoForm.vue'
import OilCaseModelForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseModelForm.vue'
import CreateRescueCaseForm from '@/views/members/form/create_case/case_child/rescue/CreateRescueCaseForm.vue'
import CreateOilCaseForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseForm.vue'
@Component({
    components: {
        // CreateOilCase,
        OilCaseInfoForm,
        OilCaseModelForm,
        CreateRescueCaseForm,
        CreateOilCaseForm
    }
})
export default class CreatedCaseForm extends Vue {
    mydata: any = null
    activeTemp = 'oil'
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
    optionWreckType: [
        {
            value: 'a'
            label: 'xx_1'
        }
    ]
    labelPosition: 'right'
    radius = 0
    nums = 100
    mounted() {}
    handleClick(tab, event) {
        console.log(tab, event)
    }
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
