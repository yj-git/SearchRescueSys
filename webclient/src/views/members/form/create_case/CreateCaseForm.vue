<template>
    <div>
        <!-- <el-dialog
            title="创建作业"
            :visible.sync="dialogVisible"
            width="45%"
            :before-close="handleClose"
        > -->
        <!-- <CreatedCaseForm ref="caseForm"></CreatedCaseForm> -->
        <!-- 此部分替换为 CreateCaseForm 组件中的部分 -->
        <el-tabs v-model="activeTemp" @tab-click="handleClick">
            <el-tab-pane label="搜救case" name="OIL">
                <CreateRescueCaseForm></CreateRescueCaseForm>

                <!-- <el-tabs :tab-position="childTablPosition">
                    <el-tab-pane label="搜救信息参数">
                        <OilCaseInfoForm></OilCaseInfoForm>
                    </el-tab-pane>
                </el-tabs> -->
            </el-tab-pane>
            <el-tab-pane label="溢油case" name="RESCUE">
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
        <!-- <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitCaseModel">确 定</el-button>
        </span> -->
        <!-- </el-dialog> -->
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
// import CreateOilCase from '@/views/members/form/CreateOilCaseForm.vue'
import OilCaseInfoForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseInfoForm.vue'
import OilCaseModelForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseModelForm.vue'
import CreateRescueCaseForm from '@/views/members/form/create_case/case_child/rescue/CreateRescueCaseForm.vue'
import CreateOilCaseForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseForm.vue'

import { CaseTypeEnum } from '@/enum/case'

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
    @Prop(Boolean)
    // dialogVisible = false
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
    handleClick(tab: { name: string }, event) {
        // index: "0" label: "搜救case" name: "OIL"
        // TODO:[-] 20-02-17 el-tab-pane 的name与 /enum/case.ts CaseTypeEnum对应！
        const caseName = tab.name
        const productType = CaseTypeEnum[caseName]
        // const productType = CaseTypeEnum.OIL
        // CaseTypeEnum[caseName]
        this.$store.dispatch('common/setProductType', productType)
        // this.$store.commit('common/SET_PRODUCT_TYPE', productType)
        // console.log(tab, event)

        // this.$store.getters('common/productType')
        console.log(this.$store.getters['common/productType'])
    }
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
