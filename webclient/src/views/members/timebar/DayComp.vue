<template>
  <div>
    <transition name="fade">
      <div class="day col-md-12">
        <div class="title">{{title}}</div>
        <div class="hours">
          <div class="hour" v-for="hour in hoursList" :key="hour.num">
            <div class="content">
              <span :class="{chosen:hour.chosen}">{{hour.num}}</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<style scoped>
.day {
  display: inline-block;
  /* background: linear-gradient(
    135deg,
    rgb(255, 246, 115),
    orange,
    rgb(207, 32, 9),
    rgb(105, 1, 105),
    rgb(3, 60, 114)
  ); */
  /* 色调修改一下 */
  /* background: linear-gradient(
    135deg,
    rgb(255, 246, 115),
    orange,
    rgb(207, 32, 9),
    rgb(105, 1, 105),
    rgb(3, 60, 114)
  ); */
  /* background: linear-gradient(135deg,rgb(88, 243, 181), rgb(57, 153, 174)); */
  /* background: linear-gradient(135deg,rgb(57, 88, 154), rgb(64, 254, 181)); */
  /* background: linear-gradient(135deg,rgb(4, 50, 142), rgb(147, 245, 240)); */
  background: linear-gradient(rgb(50, 157, 150), rgb(49, 59, 89));
  text-align: center;
  padding: 0;
  font-family: 微软雅黑;
  border-radius: 5px;
  user-select: none;
  cursor: pointer;
  color: white;
  /* padding: 5px; */
  /* width: 22em; */
  border-style: solid;
  border-width: 1px;
  border-color: gray;
  box-shadow: 1px 1px 1px black;
  margin-bottom: 5px;
  transition: 0.3s;
  /* TODO:[*] 19-11-05 字体太大了，缩小一点 */
  font-size: 0.6em;
}
.day:hover {
  box-shadow: 2px 2px 3px black;
}
.hour {
  /* height: 2em; */
  width: 2em;
  /* background: yellowgreen; */
  display: inline-block;
  margin: 0px;
  padding: 0px;
  border-width: 0px;
  text-align: center;
  line-height: 2em;
  padding: 2px;
  background: linear-gradient(
    165deg,
    rgba(255, 255, 255, 0.1),
    rgba(0, 0, 0, 0.5)
  );
}
.title {
  height: 2em;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  text-align: right;
  padding-right: 2em;
}
.chosen {
  background: rgba(0, 0, 0, 0.5);
  /* background: black; */
  display: inline-block;
  height: 100%;
  width: 100%;
  border-width: 1px;
  /* 选中不再加外边框 */
  /* border-style: solid; */

  border-radius: 0.2em;
  transition: 0.3s;
}
.chosen:hover {
  transform: scale(1.1);
}
</style>


<script>
export default {
  props: {
    index: Number,
    step: Number,
    title: String
  },
  data() {
    return {
      //   daynum: this.daynum,
      //   hours: this.hours,
      //   step: 3,
      //   index: 2,
      hoursList: [],
      daynum: "temp"
    };
  },
  watch: {
    index() {
      this.renderHours(this.step, this.index);
    },
    step() {
      this.renderHours(this.step, this.index);
    },
    title() {}
  },
  methods: {
    renderHours(step, index) {
      let list = [];
      for (let i = 0; i < 24; i++) {
        let h = i + 1;
        if (h % step == 0) {
          list.push({
            num: h,
            chosen: h / step <= index
          });
        }
      }
      this.hoursList = list;
    }
  },
  mounted() {
    this.renderHours(this.step, this.index);
  }
};
</script>
<style scoped>
</style>


