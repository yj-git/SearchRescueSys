<template>
    <div id="user-case">
        <div class="user-statistics">
            <!-- TODO:[-] 19-11-19 注意此处对组件直接通过@click绑定是无效的，需要通过@click.native进行绑定click事件 -->
            <InfoBox
                :msg="'创建case'"
                :iconstyle="'fa-edit'"
                :levelstyle="'my-default'"
                :showsize="'small'"
            ></InfoBox>
            <InfoBox
                :msg="'历史查询'"
                :iconstyle="'fa-stop-circle'"
                :levelstyle="'my-succes'"
                :showsize="'small'"
                @click.native="onClick"
            ></InfoBox>
            <InfoBox
                :msg="'风场+流场数据'"
                :iconstyle="'fa-pause-circle'"
                :levelstyle="'my-warning'"
                :showsize="'small'"
                @click.native="isShowByCoverageSearch = !isShowByCoverageSearch"
            ></InfoBox>
        </div>
        <transition name="fade">
            <div class="user-caselist" v-show="isShowByList">
                <JobList :caseList="caseList"></JobList>
            </div>
        </transition>
        <transition name="fade">
            <div class="user_caselist" v-show="isShowByCoverageSearch">
                <CoverageSearchForm></CoverageSearchForm>
            </div>
        </transition>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import InfoBox from '@/views/members/form/InfoBox.vue'
import JobListUser from '@/views/members/table/JobListByUser.vue'
import JobList from '@/views/members/table/JobListMin.vue'
import CoverageSearchForm from '@/views/members/form/search_form/CoverageSearchForm.vue'
import { ICaseMin, CaseMinInfo } from '@/middle_model/case'
@Component({
    components: { InfoBox, JobListUser, JobList, CoverageSearchForm }
})
export default class CurdBtn extends Vue {
    mydata: any = null
    isShowByList = false
    isShowByCoverageSearch = false
    @Prop()
    caseList: CaseMinInfo[]

    mounted() {}
    onClick() {
        this.isShowByList = !this.isShowByList
        // console.log('被点击了')
    }
}
</script>
<style scoped lang="less">
@import '../../../styles/base.less';
@margin: {
    margin: 0.5em;
};
.user-statistics {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
#case_list_content {
    width: 100%;
    display: flex;
    padding: 0.5em;
    // margin: 0.5em;
    flex-direction: column;
    @centerbackground();
    // 用户的统计信息
}
#user-case {
    display: flex;
    flex-direction: column;
    .user-caselist {
        width: 20em;
    }
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>
