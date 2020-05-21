<template>
    <div id="case_list_content">
        <div class="user-statistics">
            <!-- <OutLiner :count="35" :msg="'created'"></OutLiner>
      <OutLiner :count="2" :msg="'running'"></OutLiner>
      <OutLiner :count="15" :msg="'completed'"></OutLiner>
      <OutLiner :count="18" :msg="'waiting'"></OutLiner>-->
            <!-- TODO:[-] 19-11-19 注意此处对组件直接通过@click绑定是无效的，需要通过@click.native进行绑定click事件 -->
            <InfoBox
                v-for="casetemp in caseIconList"
                :key="casetemp.id"
                :count="casetemp.nums"
                :msg="casetemp.status | getStatusEnum"
                :iconstyle="casetemp.icon"
                :levelstyle="casetemp.style"
                @click.native="showDialog"
            ></InfoBox>
            <!-- <InfoBox
                :count="35"
                :msg="'created'"
                :iconstyle="'fa-edit'"
                :levelstyle="'my-default'"
                @click.native="showDialog"
            ></InfoBox>
            <InfoBox
                :count="2"
                :msg="'running'"
                :iconstyle="'fa-refresh fa-spin'"
                :levelstyle="'my-info'"
            ></InfoBox>
            <InfoBox
                :count="15"
                :msg="'completed'"
                :iconstyle="'fa-stop-circle'"
                :levelstyle="'my-succes'"
            ></InfoBox>
            <InfoBox
                :count="18"
                :msg="'waiting'"
                :iconstyle="'fa-pause-circle'"
                :levelstyle="'my-warning'"
            ></InfoBox> -->
        </div>
        <div class="case-statistics">
            <!-- 历史case的曲线图 -->
            <div class="case-history-charts">
                <CaseHistoryChart :caseDailyList="caseDailyList"></CaseHistoryChart>
            </div>
            <!-- 历史提交的case的摘要信息 -->
            <div class="case-history-form">
                <CaseHistoryForm :caseDailyList="caseDailyList"></CaseHistoryForm>
            </div>
            <!-- last10提交的case的详细信息 -->
            <div></div>
            <!-- TODO:[-] 19-11-19 以下为v1版的样式，已不使用，注释掉，暂时备份 -->
            <!-- <div class="case-listinfo">
        <div class="case-list">
          <span>当前作业列表</span>
          <JobCurrent></JobCurrent>
          <JobProgressbar
            :percent="90"
            :username="'user_1'"
            :casename="'case_xxx_1'"
            :cmt="new Date()"
          ></JobProgressbar>
        </div>

       
        <div class="user-caseinfo">
          <QueuePercent></QueuePercent>
        </div>
      </div>-->
            <!-- <div class="case-create">
        <div class="create-header">
          <h2>创建case</h2>
          <span>搜集|溢油</span>
        </div>
        <div class="create-body">
          <img src="../../../assets/create_btn.png" />
          <a>创建作业</a>
        </div>
      </div>-->
        </div>

        <div class="user-content">
            <!-- 按钮区域 -->
            <!-- <div class="buttons">
        <el-row>
          <el-button type="primary" icon="el-icon-edit" circle></el-button>
        </el-row>
      </div>
      <div class="my-table">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column label="日期" width="180">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{ scope.row.date }}</span>
            </template>
          </el-table-column>
          <el-table-column label="作业名" width="180">
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="top">
                <p>作业名: {{ scope.row.name }}</p>
                <div slot="reference" class="name-wrapper">
                  <el-tag size="medium">{{ scope.row.name }}</el-tag>
                </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="180">
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="top">
                <p>状态: {{ scope.row.state }}</p>
                <div slot="reference" class="name-wrapper"><el-tag
                    size="medium"
                    :type="scope.row.tag === 'finish' ? 'primary' : 'success'"
                    >{{ scope.row.state }}</el-tag
                  >
                </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="区域" width="180">
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="top">
                <p>区域: {{ scope.row.area }}</p>
                <div slot="reference" class="name-wrapper">
                  <el-tag size="medium">{{ scope.row.area }}</el-tag>
                </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="success"
                @click="handleEdit(scope.$index, scope.row)"
                >加载</el-button
              >
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>-->
            <JobListUser></JobListUser>
        </div>
        <!-- 新添加了创建 case 的 dialog -->
        <div class="dialog-create-case">
            <!-- TODO:[-] 20-05-19 将 el-dialog 封装至组件中 -->
            <el-dialog
                title="创建作业"
                :visible.sync="dialogVisible"
                width="45%"
                :before-close="handleClose"
            >
                <CreatedCaseForm ref="caseForm"></CreatedCaseForm>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="submitCaseModel">确 定</el-button>
                </span>
            </el-dialog>
            <!-- <CreatedCaseForm :dialogVisible="dialogVisible"></CreatedCaseForm> -->
        </div>
    </div>
</template>
<script lang="ts">
import moment from 'moment'
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
// 引入outliner
import OutLiner from '@/views/members/form/Outliner.vue'
import JobProgressbar from '@/views/members/progress/JobProgressbar.vue'
import JobCurrent from '@/views/members/table/JobCurrent.vue'
import QueuePercent from '@/views/members/percentage/QuenePercent.vue'
import InfoBox from '@/views/members/form/InfoBox.vue'
import CaseHistoryChart from '@/views/members/charts/CaseHistoryCharts.vue'
import CaseHistoryForm from '@/views/members/form/CaseHistoryForm.vue'
import JobListUser from '@/views/members/table/JobListByUser.vue'
import CreatedCaseForm from '@/views/members/form/create_case/CreateCaseForm.vue'
import { getAuthTest, loadCaseListByUser, loadCaseHistory } from '@/api/api'
import { createCaseInfo, createOilCase } from '@/api/case'
// 引入部分枚举
import { AreaEnum, getAreaVal } from '@/enum/area'
import { StatueEnum, getStatueVal } from '@/enum/status'
import { StatueInfo, IState, IDaily, CaseDailyDetail } from '@/middle_model/case'
import { AxiosResponse } from 'axios'
// TODO:[*] 20-02-17 注意此处已经将该枚举放在了统一的enum路径下，以下枚举不再使用
import { CaseTypeEnum } from '@/enum/case'
// import { ProductType } from '@/store/modules/common'
import { GET_PRODUCT_TYPE } from '@/store/types'
@Component({
    components: {
        InfoBox,
        OutLiner,
        JobProgressbar,
        JobCurrent,
        QueuePercent,
        CaseHistoryChart,
        CaseHistoryForm,
        JobListUser,
        CreatedCaseForm
    },
    // filters: {
    //     getStatusEnum(case:number):string {
    //       return ''
    //     }
    // }
    filters: {
        // TODO 时间格式化
        getStatusEnum(caseTemp: number): string {
            const temp = StatueEnum[caseTemp]
            return temp
        }
    }
})
export default class CaseListView extends Vue {
    mydata: any = null
    tableData: Array<{
        current: string
        name: string
        status: StatueEnum
        tag: string
        area: AreaEnum
    }> = []
    caseIconList: Array<StatueInfo> = []
    dialogVisible = false
    productType: CaseTypeEnum = CaseTypeEnum.OIL
    caseDailyList: Array<CaseDailyDetail> = []
    showDialog() {
        // console.log('在组件外部触发点击事件')
        this.dialogVisible = true
    }
    // 根据当前case list按照状态进行划分，为每个状态组件提供nums
    diveideCaseListByStatus(
        listCase: Array<{
            current: string
            name: string
            status: StatueEnum
            tag: string
            area: AreaEnum
        }>
    ): void {
        const listStatue: Array<StatueInfo> = []
        listStatue.push(
            new StatueInfo(StatueEnum.CREATED, 0, 1, 'fa-edit', 'my-default', 'showDialog')
        )
        listStatue.push(new StatueInfo(StatueEnum.RUNNING, 0, 2, 'fa-refresh fa-spin', 'my-info'))
        listStatue.push(new StatueInfo(StatueEnum.COMPLETED, 0, 3, 'fa-stop-circle', 'my-succes'))
        listStatue.push(new StatueInfo(StatueEnum.WAITTING, 0, 4, 'fa-pause-circle', 'my-warning'))
        // TODO:[*] 20-02-14 注意此处对ts的枚举进行遍历时，会分别将val和key都遍历出来，暂时放弃此种方式
        // for (const key in StatueEnum) {
        //     const tempEnum = StatueEnum.CREATED
        //     const temp = StatueEnum[key]
        //     const tempe = StatueEnum[parseInt(key)]
        //     console.log(`${tempEnum}|${temp}|${tempe}`)
        //     listStatue.push(new StatueInfo(tempe, 0))
        // }
        // 对传入的list进行循环分类
        listCase.forEach((temp) => {
            const stateTemp = listStatue.filter((x) => x.status === temp.status)[0]
            stateTemp.nums++
        })
        this.caseIconList = []
        this.caseIconList = listStatue
        // return listStatue
    }
    // 关闭窗口时触发
    handleClose() {}
    mounted() {
        // TODO:[*] 20-02-10 测试jwt验证
        // getAuthTest().then((res) => {
        //     console.log(res)
        // })
        this.loadCaseList()
        this.loadCaseHistory()
    }
    // 根据当前的user 获取当前user的case list
    loadCaseList(): void {
        const typeProduct: number = this.$store.state.common.productType
        loadCaseListByUser(typeProduct).then((res: AxiosResponse): void => {
            // console.log(res)
            if (res.status === 200) {
                // 获取返回的case list
                res.data.forEach(
                    (temp: {
                        name: string
                        state: number
                        area: number
                        tag: string
                        date: Date
                    }) => {
                        const dateTemp = moment(temp.date)
                        const dateTarget = dateTemp.format('YYYY-MM-DD')
                        this.tableData.push({
                            ...temp,
                            current: dateTarget,
                            area: temp.area, // 注意直接使用enum中的对应的number，赋值给枚举类型的实例
                            status: temp.state
                        })
                    }
                )
                this.diveideCaseListByStatus(this.tableData)
            }
        })
    }
    loadCaseHistory(): void {
        // const type: ProductType = this.$store.commit(GET_PRODUCT_TYPE)
        const type: CaseTypeEnum = this.$store.getters['common/productType']
        this.productType = type
        // console.log(type)
        loadCaseHistory(type).then((res) => {
            if (res.status === 200) {
                console.log(res.data)
                res.data.forEach((temp) => {
                    if ('date' in temp && 'nums' in temp)
                        this.caseDailyList.push(new CaseDailyDetail(new Date(temp.date), temp.nums))
                })
            }
        })
    }

    // 在父组件中进行提交操作
    // TODO:[-] 20-02-16 获取嵌套的子组件中绑定的data
    submitCaseModel(): void {
        // TODO:[-] 20-02-16 获取嵌套组件中的data
        const formInfo: any = this.$refs.caseForm.$refs.oil.$refs.infoForm.form
        const formModel: any = this.$refs.caseForm.$refs.oil.$refs.modelForm.form
        const submitForm = { ...formInfo, ...formModel }
        console.log(submitForm)
        // createCaseInfo(,submitForm)
        // TODO:[*] 20-05-19 完成提交操作
        createOilCase(submitForm)
    }
    get computedTest() {
        return null
    }
}
</script>
<style scoped lang="less">
@import '../../../styles/base.less';
@margin: {
    margin: 0.5em;
};
#case_list_content {
    width: 100%;
    display: flex;
    padding: 0.5em;
    // margin: 0.5em;
    flex-direction: column;
    @centerbackground();
    // 用户的统计信息
    .user-statistics {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
    }
    // 作业的统计信息
    .case-statistics {
        // height: 500px;
        // background: rgb(189, 123, 123);
        display: flex;
        @margin();
        justify-content: center;
        // flex-direction: row;
        .case-history-charts {
            height: 500px;

            @formbox();
        }
        // 以下两个样式暂时不再使用
        .case-listinfo {
            display: flex;
            flex: 4;
            // height: 400px;
            background: red;
            // flex-direction:
            .case-list {
                background: yellow;
                display: flex;
                flex: 2;
                flex-direction: column;
                margin: 1em;
                @allradius();
                div {
                    margin: 1em;
                }
                span {
                    display: flex;
                    justify-content: flex-start;
                    align-items: flex-start;
                    margin: 1em;
                    color: black;
                    font-size: 100%;
                }
                // flex
            }
            .user-caseinfo {
                display: flex;
                background: rgb(146, 146, 69);
                flex: 1;
            }
        }
        // 创建的按钮
        .case-create {
            display: flex;
            flex-direction: column;
            flex: 1;
            height: 400px;
            // background: green;
            // align-items: center;
            justify-content: center;
            .create-header {
                // background-color: #2bbbad !important;
                background: linear-gradient(40deg, #45cafc, #303f9f) !important;
                // @allradius();
                padding: 1.5em;
                box-shadow: 5px 5px 15px #333333;
            }
            .create-body {
                height: 15em;
                // background: blue;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-right: 4%;
                margin-left: 4%;
                box-shadow: 5px 5px 15px #333333;
                // @allradius();
                img {
                    height: 8em;
                    @margin();
                }
                span {
                    @margin();
                }
                button {
                    height: 4em;
                    width: 4em;
                    @allradius();
                    @margin();
                }
                // 不再使用bt的btn，改为自己实现的a标签
                a {
                    display: inline-block;
                    background-color: #880e4f !important;
                    padding: 1em;
                    border-radius: 0.125rem;
                    box-shadow: 5px 5px 15px #333333;
                }
                a:hover {
                    box-shadow: 0 5px 11px 0 rgba(0, 0, 0, 0.18), 0 4px 15px 0 rgba(0, 0, 0, 0.15);
                }
            }
        }
    }
    .user-content {
        display: flex !important;
        justify-content: center;
        align-items: center;
        // width: 70%;
    }
    //
}
</style>
