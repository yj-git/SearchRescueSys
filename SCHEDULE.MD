---
19-08-21
- [x] 1.修改了前台使用 vue2-leaflet 组件时，更新 url 而未刷新的问题
- [x] 2.改为将 wms-tile-layer 依托数组的方式
---

19-08-22

- [x] 1.由 timebar 像 windMap 的传递
- [ ] 2.  加入 timebar 的设计，未完成，晚上继续

---

19-08-23

- [x] 1. timebar 由 data 中的 datalist 来动态生成长度
- [x] 2. 完成 timebar 的功能
- [ ] 3. 部分遇见的问题待总结

---

19-09-03

- [x] 1. 完成对搜救 nc 文件的录入操作
- [ ] 2. 前端展示

---

19-09-17

- [ ] 1. 读取溢油数据
- [ ] 2. 设计mongo中相关库表

---
之后进度部分未更新

---
19-10-31
- [x] 前端完成点击`OilSpillingMap`更新`oilAvgRealData`并prop的方式传递给子组件
- [x] 后端加入相应接口
- [x] 组件设计如下
   ![alt 组件1](./document/99img/TIM截图20191031213012.png)
   ![alt 组件2](./document/99img/TIM截图20191031213043.png)


---
19-11-07 
- [x] 前端完成`src\views\content\oilspilling\oilSpillingMap.vue`与`src\views\bar\oilRightBar.vue`组件的联动，修改了之前存在的部分bug

---
19-11-13
- [x] 溢油完成了load时清除 heat与散点图
- [x] 样式统一修改 

---
19-11-14
- [x] 搜救和溢油的界面样式统一，使用less加入了部分父类变量
- [ ] 恢复之前的搜救页面的散点图的加载功能

---
19-11-18-20
- [x] 重构了作业列表页面
- [x] 加入了当前用户的作业状态
- [x] 历史作业状态
- [x] 作业列表
   ![alt 实现效果](./document/99img/TIM截图20191120143602.png)

---
19-11-21 
- [x] 重构了溢油子页面
  ![alt 实现效果](./document/99img/微信图片_20191121224611.png)
- [ ] 缺少部分效果

---
19-11-28  
- [x] 重新加入了job的相关proj
![alt job思维导图](./document/99img/background/job.png)
![alt 泳道](./document/99img/background/TIM截图20191128221450.png)

---
19-12-26  
* 中间有部分的更新记录为在进度中更新
- [x] 重构了读取溢油的nc文件并写入数据库的相关逻辑，才用了一个时间间隔，一次批量写入数据库的操作
* 性能提升明显，耗时: 2121.70 -> 378.09