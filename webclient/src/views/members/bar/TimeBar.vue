<template>
  <div class="dateBar">
    <div class="progress-line" @mouseover="setProgressLine">
      <div id="played" class="played" style="width: 10px;"></div>
      <div class="avbl"></div>
      <i style="left: 85.6454px;"></i>
    </div>
    <div id="playpause" class="play-pause iconfont clickable off"></div>
    <div id="calendar">
      <div class v-for="item in datelist" :key="item.id">{{item.label}}</div>
    </div>
    <div id="msg">{{slideDateLabelr}}</div>
    <div id="staticmsg">{{staticDateLabel}}</div>
  </div>
</template>
<script lang='ts'>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
@Component({})
export default class center_map extends Vue {
  mydata: any = null;
  datelist: Array<any> = [
    {
      // value: 0,
      label: "01日",
      children: [
        {
          value: 0,
          label: "01-00时"
        },
        {
          value: 1,
          label: "01-06时"
        },
        {
          value: 2,
          label: "01-12时"
        },
        {
          value: 3,
          label: "01-18时"
        }
      ]
    },
    {
      // value: 0,
      label: "02日",
      children: [
        {
          value: 4,
          label: "02-00时"
        },
        {
          value: 5,
          label: "02-06时"
        },
        {
          value: 6,
          label: "02-12时"
        },
        {
          value: 7,
          label: "02-18时"
        }
      ]
    },
    {
      // value: 0,
      label: "03日",
      children: [
        {
          value: 8,
          label: "03-00时"
        },
        {
          value: 9,
          label: "03-06时"
        },
        {
          value: 10,
          label: "03-12时"
        },
        {
          value: 11,
          label: "03-18时"
        }
      ]
    }
  ];
  // 选中的时间在datelist中对应的obj
  selectDate: any = null;
  selectHour: String = "";
  // 滑动时显示的日期label
  slideDateLabelr: String = "";
  // 点击后固定在点击处的日期label
  staticDateLabel: String = "";

  prefixInteger(num: String, length: String): String {
    return ("0000000000000000" + num).substr(-length);
  }

  // 鼠标移入时间line时的操作
  setProgressLine(event: any): void {
    console.log(this);
    console.log(event);
    var myself = this;
    var mainDom = document.getElementsByClassName("progress-line");
    // 1 计算整个进度条的长度
    var lenTotal = event.currentTarget.clientWidth;
    // 2-1 计算后除以41分
    // 2-2计算每一个格子的宽度
    var cellWidth = lenTotal / 41;
    // 3 获取鼠标选中的点的位置
    var lenTarget = event.offsetX;
    // 4 然后获取该位置属于的格子
    var indexTarget = lenTarget / cellWidth;
    var indexTargetCell = indexTarget;

    // 4-s1 根据格子的位置获取该日的位置
    var unit = 4;
    var indexDate = indexTargetCell / unit;
    // 5 将进度条中的填色部分宽度改变
    var playedDom = document.getElementById("played");
    if (playedDom != null) {
      playedDom.style.width = event.offsetX + ".px";
    }

    // 6 显示数值
    // 6-s1 根据选中的日期获取该日所在的位置的数值，以及children中的label
    var dateTemp = myself.datelist[indexDate].children.filter(obj => {
      return obj.value === indexTargetCell;
    });
    // 判断获取的dateTemp是否长度为1
    if (dateTemp.length === 1) {
      dateTemp = dateTemp[0];
      myself.slideDateLabelr = dateTemp.label;
      // myself.selectDate = dateTemp
      var msg = document.getElementById("msg");
      if (msg != null) {
        msg.style.display = "block";
        msg.style.left = event.offsetX + 10 + ".px";
        // msg.style.top = e.clientY - 35 + ".px";
        // 注意在vue组件中，若使用绝对定位，若在style中使用了scoped，则这个绝对定位是针对当前组件而言的
        msg.style.top = event.offsetY - 35 + ".px";
      }
    }
    // msg.innerText = dates[indexTarget];
    // msg.html(dates[indexTarget]);
    // console.log(indexTarget)
  }
  mounted() {
    var myself = this;
    // 鼠标点击抬起
    // $(".progress-line").mouseup(function(e) {
    //   // console.log(e)
    //   // 1 计算整个进度条的长度
    //   var lenTotal = e.currentTarget.clientWidth;
    //   // 2-1 计算后除以41分
    //   // 2-2计算每一个格子的宽度
    //   var cellWidth = lenTotal / 41;
    //   // 3 获取鼠标选中的点的位置
    //   var lenTarget = e.offsetX;
    //   // 4 然后获取该位置属于的格子
    //   var indexTargetCell:number = lenTarget / cellWidth;
    // //   indexTargetCell = parseInt(indexTargetCell);
    //   // 4-s1 根据格子的位置获取该日的位置
    //   var unit = 4;
    //   var indexDate:number = indexTargetCell / unit;
    //   // 5 将进度条中的填色部分宽度改变
    //   document.getElementsByClassName("played")[0].style.width =
    //     e.offsetX + ".px";
    //   // 6 显示数值
    //   // 6-s1 根据选中的日期获取该日所在的位置的数值，以及children中的label
    //   // var dateTemp = myself.datelist[indexDate].children.map(obj => {
    //   //   if (obj.value === indexTargetCell) {
    //   //     return obj
    //   //   }
    //   // })
    //   var dateTemp = myself.datelist[indexDate].children.filter(obj => {
    //     // if (obj.value === indexTargetCell) {
    //     //   return obj
    //     // }
    //     return obj.value === indexTargetCell;
    //   });
    //   // 判断获取的dateTemp是否长度为1
    //   if (dateTemp.length === 1) {
    //     dateTemp = dateTemp[0];
    //     myself.staticDateLabel = dateTemp.label;
    //     myself.selectDate = dateTemp;
    //     var msg = document.getElementById("staticmsg");
    //     msg.style.display = "block";
    //     msg.style.left = e.offsetX + 10 + ".px";
    //     // msg.style.top = e.clientY - 45 + '.px'
    //     msg.style.top = e.offsetY - 45 + ".px";

    //     // 触发父组件中的方法，或修改父组件中的值
    //     var layerIndex = myself.prefixInteger(str(indexTargetCell) * 6, 3);
    //     myself.$emit("changeLayerIndex", layerIndex);
    //   }
    // });

    // 鼠标移动
    // var mainDom = document.getElementsByClassName("progress-line");
    // $(".progress-line").mousemove(function(e) {
    //   // console.log(e)
    //   // 1 计算整个进度条的长度
    //   var lenTotal = e.currentTarget.clientWidth;
    //   // 2-1 计算后除以41分
    //   // 2-2计算每一个格子的宽度
    //   var cellWidth = lenTotal / 41;
    //   // 3 获取鼠标选中的点的位置
    //   var lenTarget = e.offsetX;
    //   // 4 然后获取该位置属于的格子
    //   var indexTarget = lenTarget / cellWidth;
    //   var indexTargetCell = parseInt(indexTarget);

    //   // 4-s1 根据格子的位置获取该日的位置
    //   var unit = 4;
    //   var indexDate = parseInt(indexTargetCell / unit);
    //   // 5 将进度条中的填色部分宽度改变
    //   document.getElementsByClassName("played")[0].style.width =
    //     e.offsetX + ".px";
    //   // 6 显示数值
    //   // 6-s1 根据选中的日期获取该日所在的位置的数值，以及children中的label
    //   var dateTemp = myself.datelist[indexDate].children.filter(obj => {
    //     return obj.value === indexTargetCell;
    //   });
    //   // 判断获取的dateTemp是否长度为1
    //   if (dateTemp.length === 1) {
    //     dateTemp = dateTemp[0];
    //     myself.slideDateLabelr = dateTemp.label;
    //     // myself.selectDate = dateTemp
    //     var msg = document.getElementById("msg");
    //     msg.style.display = "block";
    //     msg.style.left = e.offsetX + 10 + ".px";
    //     // msg.style.top = e.clientY - 35 + ".px";
    //     // 注意在vue组件中，若使用绝对定位，若在style中使用了scoped，则这个绝对定位是针对当前组件而言的
    //     msg.style.top = e.offsetY - 35 + ".px";
    //   }
    //   // msg.innerText = dates[indexTarget];
    //   // msg.html(dates[indexTarget]);
    //   // console.log(indexTarget)
    // });
  }
  get computedTest() {
    return null;
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
  bottom: 50px;
  white-space: nowrap;
  width: 500px;
}

#calendar {
}

#calendar div {
  display: inline-block;
  box-sizing: border-box;
  text-align: left;
  padding: 6px 0 0 8px;
  font-size: 12px;
  line-height: 1;
  height: 26px;
  white-space: nowrap;
  overflow: hidden;
  width: 30%;
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
  text-shadow: 2px 2px 10px #000;
  border-radius: 2px;
}
</style>
