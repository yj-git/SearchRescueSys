<template>
    <div>
        <el-tabs :tab-position="childTablPosition">
            <el-tab-pane label="搜救信息参数">
                <OilCaseInfoForm ref="infoForm"></OilCaseInfoForm>
            </el-tab-pane>
            <el-tab-pane label="模型参数">
                <OilCaseModelForm ref="modelForm"></OilCaseModelForm>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import OilCaseInfoForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseInfoForm.vue'
import OilCaseModelForm from '@/views/members/form/create_case/case_child/oil/CreateOilCaseModelForm.vue'

@Component({
    components: {
        OilCaseInfoForm,
        OilCaseModelForm
    }
})
export default class CreateOilCaseForm extends Vue {
    mydata: any = null
    mounted() {}
    childTablPosition = 'left'
    get computedTest() {
        return null
    }
}
</script>
<style scoped></style>
