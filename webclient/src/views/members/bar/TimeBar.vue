<template>
    <div class="dateBar">
        <div class="progress-line" @mouseover="overProgressLine" @click="setTimeBar">
            <div id="played" class="played" style="width: 10px;"></div>
            <div class="avbl"></div>
            <i style="left: 85.6454px;"></i>
        </div>
        <div id="playpause" class="play-pause iconfont clickable off"></div>
        <div id="calendar">
            <!-- <div class v-for="item in datelist" :key="item.id">{{item.dateStr()}}</div> -->
            <div class="calendar_interval">
                <div
                    v-for="item in cellArr"
                    :key="item.id"
                    :style="'width:' + lenUnit + 'px;'"
                ></div>
            </div>

            <!-- <div
        class="calendar_cutting_line"
        v-for="item in cellArr"
        :key="item.id"
        :style="'width:'+ (lenUnit) +'px;'"
      ></div>-->
            <div class="calendar_cutting_line">
                <div
                    v-for="(item, index) in cuttingLinesWidth"
                    :key="item.id"
                    :style="'width:' + lenUnit * item + 'px;'"
                >
                    {{ cuttingLinesIndex[index] }}小时
                </div>
            </div>
        </div>
        <div id="msg">{{ slideDateLabelr }}</div>
        <div id="staticmsg">{{ staticDateLabel }}</div>
    </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'

import { Mutation, State, namespace } from 'vuex-class'

import { DateModel } from '@/model/bar/timebar'
import { SET_MAP_NOW } from '@/store/types'
import moment from 'moment'
import dateformat from 'dateformat'
@Component({})
export default class TimeBar extends Vue {
    mydata: any = null
    datelist: Array<DateModel> = []
    // 每个格子对应的datelist
    datetimelist: Array<Date> = []
    // 选中的时间在datelist中对应的obj
    selectDate: any = null
    selectHour = ''
    // 滑动时显示的日期label
    slideDateLabelr = ''
    // 点击后固定在点击处的日期label
    staticDateLabel = ''
    hoverCurrentDt: Date = new Date(1970, 1, 1)
    selectedCurrentDt: Date = new Date(1970, 1, 1)
    // TODO:[*] 19-09-12 新加入的复用子组件的需要用到的一些变量
    lenTimeBar = 600
    // 起始偏移位置
    siteStart: number
    // 每日共划分的间隔
    // intervalOfDay: number;

    // 共显示的天数
    // days: number;
    // 计算属性计算出lenUnit——单位格子的长度
    get lenUnit(): number {
        if (this.interval != 0) {
            return this.lenTimeBar / this.countUnit
        } else {
            return 0
        }
    }
    // 计算：第一个完整的00时所在的格子
    get startIndex(): number {
        return this.diff2StartDayFinish * (24 / this.interval)
    }
    // 计算：获取总格子数
    get countUnit(): number {
        // TODO:[*] 19-09-12 注意此处不需要这么计算直接根据days来计算即可，因为总共只有days天的数据
        // return (
        //   this.days * this.interval +
        //   this.diff2StartDayFinish / (24 / this.interval)
        // );
        return this.days * this.interval
    }

    get cellArr(): number[] {
        // TODO:[*] 19-09-12 快速创建长度为100的数组
        return [...Array(this.countUnit).keys()]
    }

    // 计算：获取分割线数组
    get cuttingLinesIndex(): number[] {
        const nums: number[] = []
        nums.push(0)
        nums.push(this.startIndex)
        if (this.days > 1) {
            for (let index = 1; index <= this.days; index++) {
                // const element = array[index];
                nums.push(index * (24 / this.intervalStamp))
            }
        }

        return nums
    }

    get cuttingLinesWidth(): number[] {
        const nums: number[] = []

        nums.push(this.startIndex)
        if (this.days > 1) {
            for (let index = 1; index <= this.days; index++) {
                nums.push(24 / this.intervalStamp)
            }
        }

        return nums
    }
    // 计算：起始时间距离第一天结束的时间差（hour）
    get diff2StartDayFinish(): number {
        return 24 - this.targetDate.getHours()
    }

    prefixInteger(num: string, length: string): string {
        return ('0000000000000000' + num).substr(-length)
    }

    @Prop(Date)
    // targetDate?: Date;
    targetDate!: Date

    @Prop(Number)
    days!: number
    //每日共划分的间隔
    @Prop(Number)
    interval!: number

    //每个间隔的小时（单位：小时）
    get intervalStamp(): number {
        return 24 / this.interval
    }
    // 鼠标移入时间line时的操作
    overProgressLineBak(event: any): void {
        // console.log(this);
        // console.log(event);
        const myself = this
        const mainDom = document.getElementsByClassName('progress-line')
        // 1 计算整个进度条的长度
        const lenTotal = event.currentTarget.clientWidth
        // 2-1 计算后除以12份（计算72小时的，间隔6小时一个，共12个格子）
        // 2-2计算每一个格子的宽度
        // TODO:[*] 19-09-10 修改格子的间隔为每小时一个格子
        // var cellWidth = lenTotal / 12;
        const cellWidth = this.lenUnit
        // 3 获取鼠标选中的点的位置
        const lenTarget = event.offsetX
        // 4 然后获取该位置属于的格子
        const indexTarget = lenTarget / cellWidth
        const indexTargetCell = parseInt(indexTarget.toString())

        // 4-s1 根据格子的位置获取该日的位置
        const unit = 4
        const indexDate = parseInt((indexTargetCell / unit).toString())
        // 5 将进度条中的填色部分宽度改变
        const playedDom = document.getElementById('played')
        if (playedDom != null) {
            playedDom.style.width = event.offsetX + '.px'
        }

        // 6 显示数值
        // 6-s1 根据选中的日期获取该日所在的位置的数值，以及children中的label
        const dateTemp = myself.datelist[indexTargetCell].children.filter((obj: any) => {
            return obj.value === indexTargetCell
        })
        // 判断获取的dateTemp是否长度为1
        if (dateTemp.length === 1) {
            const currentDate = dateTemp[0]
            myself.hoverCurrentDt = currentDate.date
            // myself.tempCurrentDt=currentDate.
            myself.slideDateLabelr = currentDate.datetimeStr()
            // myself.selectDate = dateTemp
            const msg = document.getElementById('msg')
            if (msg != null) {
                msg.style.display = 'block'
                msg.style.left = event.offsetX + 10 + '.px'
                // msg.style.top = e.clientY - 35 + ".px";
                // 注意在vue组件中，若使用绝对定位，若在style中使用了scoped，则这个绝对定位是针对当前组件而言的
                msg.style.top = event.offsetY - 35 + '.px'
            }
        }
        // msg.innerText = dates[indexTarget];
        // msg.html(dates[indexTarget]);
        // console.log(indexTarget)
    }

    overProgressLine(event: any): void {
        const myself = this
        const mainDom = document.getElementsByClassName('progress-line')
        // 1 计算整个进度条的长度
        const lenTotal = event.currentTarget.clientWidth
        // 2-1 计算后除以12份（计算72小时的，间隔6小时一个，共12个格子）
        // 2-2计算每一个格子的宽度
        // TODO:[*] 19-09-10 修改格子的间隔为每小时一个格子
        // var cellWidth = lenTotal / 12;
        const cellWidth = this.lenUnit
        // 3 获取鼠标选中的点的位置
        const lenTarget = event.offsetX
        // 4 然后获取该位置属于的格子
        const indexTarget = lenTarget / cellWidth
        const indexTargetCell = parseInt(indexTarget.toString())

        // 4-s1 根据格子的位置获取该日的位置
        const unit = 4
        const indexDate = parseInt((indexTargetCell / unit).toString())
        // 5 将进度条中的填色部分宽度改变
        const playedDom = document.getElementById('played')
        if (playedDom != null) {
            playedDom.style.width = event.offsetX + '.px'
        }

        // 6 显示数值
        // V1
        // 6-s1 根据选中的日期获取该日所在的位置的数值，以及children中的label
        // var dateTemp = myself.datelist[indexTargetCell].children.filter(
        //   (obj: any) => {
        //     return obj.value === indexTargetCell;
        //   }
        // );
        // // 判断获取的dateTemp是否长度为1
        // if (dateTemp.length === 1) {
        //   let currentDate = dateTemp[0];
        //   myself.hoverCurrentDt = currentDate.date;
        //   // myself.tempCurrentDt=currentDate.
        //   myself.slideDateLabelr = currentDate.datetimeStr();
        //   // myself.selectDate = dateTemp
        //   var msg = document.getElementById("msg");
        //   if (msg != null) {
        //     msg.style.display = "block";
        //     msg.style.left = event.offsetX + 10 + ".px";
        //     // msg.style.top = e.clientY - 35 + ".px";
        //     // 注意在vue组件中，若使用绝对定位，若在style中使用了scoped，则这个绝对定位是针对当前组件而言的
        //     msg.style.top = event.offsetY - 35 + ".px";
        //   }
        // }
        // TODO:[*] 19-09-12 使用v2方法
        const dateTemp = this.datetimelist[indexTargetCell]

        const currentDate = dateTemp
        myself.hoverCurrentDt = currentDate
        // myself.tempCurrentDt=currentDate.
        myself.slideDateLabelr = dateformat(currentDate, 'mm/dd HH:MM')
        // myself.selectDate = dateTemp
        const msg = document.getElementById('msg')
        if (msg != null) {
            msg.style.display = 'block'
            msg.style.left = event.offsetX + 10 + '.px'
            // msg.style.top = e.clientY - 35 + ".px";
            // 注意在vue组件中，若使用绝对定位，若在style中使用了scoped，则这个绝对定位是针对当前组件而言的
            msg.style.top = event.offsetY - 35 + '.px'
        }
    }
    setTimeBar(event: any): void {
        // console.log('点击事件')
        // 点击之后更新这个选中的时间
        this.selectedCurrentDt = this.hoverCurrentDt
    }
    initDateList(): void {
        // this.moment()
        //TODO:[*] 注意new Date时，month为从0开始
        // var currentTemp = new Date(1990, 0, 1, 0, 0);
        // var currentTemp = new Date(2016, 6, 20, 12, 0);
        const currentTemp = this.targetDate
        // 转换成时间戳
        const currentStamp = currentTemp.getTime()

        const tempTimeStampInterval: number = this.intervalStamp * 60 * 60 * 1000
        const countIntervalByDay = this.interval
        // var temp = currentTemp.setHours(currentTemp.getHours() + 6);
        // console.log(temp);
        for (let i = 0; i < this.days; i++) {
            // 直接加一天
            this.datelist.push(
                new DateModel(i, new Date(currentStamp + i * 24 * 60 * 60 * 1000), [])
            )
            for (let j = 0; j < countIntervalByDay; j++) {
                this.datelist[i].children.push(
                    new DateModel(
                        i * countIntervalByDay + j,
                        new Date(currentStamp + j * tempTimeStampInterval)
                    )
                )
            }
        }
    }

    // TODO:[*] 19-09-12 每个格子对应的 date list
    initDateTimeList(): void {
        // 根据 起始时间——targetDate，总共的天数——days，每日的间隔——interval 共同计算

        // 每个单元格在时间上的间隔
        const intervalUnit = 24 / this.interval
        const startStamp = this.targetDate.getTime()
        // 每个间隔的间隔时间（ms）
        const tempTimeInterval: number = (24 / this.interval) * 60 * 60 * 1000
        for (let index = 0; index < this.countUnit; index++) {
            this.datetimelist.push(new Date(startStamp + index * tempTimeInterval))
        }
    }

    // 为时间分割线设置起始位置
    initCuttingLinesClass(): void {
        // 找到日期分个符的外侧div
        const calendarDom = document.getElementById('calendar')
        if (calendarDom != null) {
            // TODO:[*] 19-09-12 注意此时的calendar dom并没有子节点
            // 找到第一个子div设置left的偏移
            const child: HTMLElement = calendarDom.childNodes[1] as HTMLElement
            // eg: 第一个为8，8*格子的宽度
            child.style['left'] = this.cuttingLinesIndex[1] * this.lenUnit + 'px'
            if (calendarDom.childNodes.length > 1) {
                // 其余的子div设置宽度
                // 从数组中刨除位置为0的
                const arr = calendarDom.childNodes
                // TODO:[*] 19-09-12 注意此处的arr是NodeList而并不是array！！注意
                /*
          参考文章：
          https://gomakethings.com/converting-a-nodelist-to-an-array-with-vanilla-javascript/
          使用方法：
          Array.from()
          注意此方法不适用于ie
        */
                let tempArr = Array.from(arr)
                const lastIndex = tempArr.length - 1
                tempArr = tempArr.slice(1, lastIndex)
                tempArr.forEach((temp: ChildNode) => {
                    ;(temp as HTMLElement).style.width = this.lenUnit * this.interval + 'px'
                    // temp.style.width = this.lenUnit * this.interval + "px";
                })
            }
        }
    }

    // 为所有的cell添加样式（实际就是宽度）
    initCellArrClass(): void {}

    mounted() {
        // var myself = this;
    }
    get computedTest() {
        return null
    }

    @Mutation('setcurrent', { namespace: 'map' }) setCurrent

    // TODO:[-] 20-02-20
    @Mutation(SET_MAP_NOW, { namespace: 'map' }) setNow

    @Watch('selectedCurrentDt')
    onSelectedCurrentDt(dt: Date): void {
        // 当修改 当前选中的dt 修改vuex中的对应的值
        // 修改vuex中的 current （注意：current为str类型）
        // TODO:[*] 注意此处
        /*
      dt:Thu Feb 01 1990 12:00:00 GMT+0800 (中国标准时间)
      dt.toUTCString():
        "Thu, 01 Feb 1990 04:00:00 GMT"
      dt.toISOString():
        "1990-02-01T04:00:00.000Z"
    */

        //TODO:[*] 19-11-12 以vuex-class的方式调用mutation
        // this.$store.commit("current", dt.toISOString());
        // this.setCurrent(dt.toISOString())
        this.setNow(dt)
    }
    @Watch('datelist')
    onDateList(): void {
        // 当监听到datelist发生变化时，等该dom渲染完毕后再执行
        const myself = this
        this.$nextTick(function() {
            // myself.initCuttingLinesClass();
        })
    }

    @Watch('targetDate')
    onTargetDate(val: Date): void {
        console.log(`修改了targetDate:${val}`)

        // TODO:[*] 19-09-12 为了避免父组件还未为prop赋值子组件就执行mounted方法初始化监听的 targetDate prop，把它放在监听方法中
        // 初始化时间列表
        this.initDateList()
        // 初始化每个间隔的时间列表
        this.initDateTimeList()
    }
}
</script>
<style scoped>
.dateDiv {
    /* position: absolute; */
    /* bottom: 100px; */
    /* left: 250px; */
    z-index: 999;
    background: #29242168;
    /* width:  */
    box-shadow: 0 20px 10px -11px #35312e68;
    border-radius: 2.5px;

    display: flex;
    /* 主轴对其方式 */
    justify-content: center;
    /* 交叉轴对其方式 */
    align-items: center;
    height: 50px;
}

.dateBar {
    z-index: 999;
    position: absolute;
    left: 250px;
    right: 0;
    bottom: 90px;
    white-space: nowrap;
    width: 600px;
}

#calendar {
    top: -20px;
    position: absolute;
}

.calendar_cutting_line {
}

.calendar_cutting_line_test {
    position: absolute;
    display: inline-block;
    box-sizing: border-box;
    text-align: left;
    padding: 6px 0 0 8px;
    font-size: 12px;
    line-height: 1;
    height: 26px;
    white-space: nowrap;
    overflow: hidden;
    /* width: 30%; */
    /*字体*/
    text-shadow: 0 0 4px black;
    color: #fff3e1;
    /*加入边框样式*/
    border-left: 1px solid black;
    /*border-right:1px solid black;*/
}
.calendar_interval {
    position: absolute;
}
.calendar_interval div {
    /* position: absolute; */
    display: inline-block;
    box-sizing: border-box;
    text-align: left;
    padding: 6px 0 0 8px;
    font-size: 8px;
    line-height: 1;
    height: 8px;
    white-space: nowrap;
    overflow: hidden;
    /* width: 30%; */
    /*字体*/
    text-shadow: 0 0 4px black;
    color: #fff3e1;
    /*加入边框样式*/
    border-left: 1px solid rgb(146, 158, 74);
    /*border-right:1px solid black;*/
}
.calendar_cutting_line {
    position: absolute;
    top: 30px;
}
.calendar_cutting_line div {
    /* position: absolute; */
    display: inline-block;
    box-sizing: border-box;
    text-align: left;
    padding: 6px 0 0 8px;
    font-size: 12px;
    line-height: 1;
    height: 26px;
    white-space: nowrap;
    overflow: hidden;
    /* width: 30%; */
    /*字体*/
    text-shadow: 0 0 4px black;
    color: #fff3e1;
    /*加入边框样式*/
    border-left: 1px solid black;
    /*border-right:1px solid black;*/
}
#playpause {
    position: absolute;
    top: -12px;
    left: -35px;
    z-index: 10;
}

.play-pause {
    display: block;
    font-size: 25px;
    color: #9d0300;
    width: 1.2em;
    height: 1.2em;
    border-radius: 1.2em;
    box-shadow: 0 0 4px 0 black;
    background-color: #e5e5e5;
}

.progress-line {
    height: 6px;
    cursor: pointer;
    position: relative;
    border: 10px solid transparent;
    border-right-color: transparent;
    border-right-style: solid;
    border-right-width: 10px;
    border-left-color: transparent;
    border-left-style: solid;
    border-left-width: 10px;
    background-clip: padding-box;
    border-right: none;
    border-left: none;
    top: -10px;
    -webkit-transition: width ease-in-out 0.7s;
    transition: width ease-in-out 0.7s;
}

.progress-line .played {
    background-color: #e5e5e5;
    height: 6px;
    float: left;
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
    width: 15%;
}

.progress-line .avbl {
    height: 6px;
    background-color: rgba(0, 0, 0, 0.6);
    width: 100%;
    border-radius: 6px;
}

#msg {
    position: absolute;
    display: none;
    color: rgb(231, 180, 40);
}
#staticmsg {
    position: absolute;
    display: none;
    background: #1bc5a3;
    border-radius: 0.5em;

    /*字体*/
    text-shadow: 0 0 4px black;
    color: #fff3e1;
}
/* 以下暂时不用了 */
/* #date {
  width: 150px;
} */
.row {
    margin-right: 0px;
    margin-left: 0px;
    display: flex;
    /* 主轴对其方式 */
    justify-content: center;
    /* 交叉轴对其方式 */
    align-items: center;
}
.row > div {
    margin-right: 3px;
    margin-left: 3px;
}
.dateDiv > .row > .title {
    color: rgb(175, 184, 191);
    font-size: 2em;
    font-weight: bold;
    text-shadow: 2px 2px 10px rgb(220, 243, 14);
    border-radius: 2px;
}
</style>
