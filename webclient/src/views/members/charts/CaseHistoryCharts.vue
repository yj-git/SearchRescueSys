<template>
    <div id="history-chart"></div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import echarts from 'echarts'
// import 'moment'
import { CaseDailyDetail } from '@/middle_model/case'
import moment from 'moment'
@Component({})
export default class CaseHistoryChart extends Vue {
    mychart: any = null
    dataChart: Array<string> = []
    numsChart: Array<number> = []

    @Prop()
    caseDailyList: Array<CaseDailyDetail>
    mounted() {
        this.initChart()
    }

    initChart() {
        // 基于准备好的dom，初始化echarts图表
        const myself = this
        myself.mychart = null
        const option = {
            xAxis: {
                type: 'category',
                data: myself.dataChart
            },
            yAxis: {
                type: 'value'
            },
            backgroundColor: '#2c343c',
            textStyle: {
                color: 'rgba(255, 255, 255, 0.3)'
            },
            color: 'rgb(65, 238, 200)',
            series: [
                {
                    data: myself.numsChart,
                    type: 'line'
                }
            ]
        }
        if (myself.mychart === null) {
        }
        const chart = document.getElementById('history-chart') as HTMLDivElement
        // TODO:[*] 19-11-19
        /*
        Argument of type 'HTMLElement | null'
        is not assignable to parameter of type 'HTMLDivElement | HTMLCanvasElement'.
         Type 'null' is not assignable to type 'HTMLDivElement | HTMLCanvasElement'.
    */
        if (chart != null) {
            myself.mychart = echarts.init(chart)
            myself.mychart.setOption(option)
        }
    }
    private clearChartData(): void {
        this.dataChart = []
        this.numsChart = []
    }
    get computedTest() {
        return null
    }

    @Watch('caseDailyList', { deep: true })
    onCaseDailyList(val: Array<CaseDailyDetail>): void {
        // 将case daily list进行拆分
        this.clearChartData()
        val.forEach((temp) => {
            this.dataChart.push(moment(temp.current).format('L'))
            this.numsChart.push(temp.nums)
        })
        this.initChart()
    }
}
</script>
<style scoped lang="less">
#history-chart {
    height: 500px;
    width: 800px;
    //   background:rgb(65, 238, 200);
}
</style>
