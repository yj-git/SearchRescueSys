import Vue from "vue";

import App from "./App.vue";

import router from "./router";
// TODO:[*] 19-11-08 修改路径为store路径下，不再是index.ts，可能导致之前的一些问题
import store from "./store/index";
// import store from "./store";

// import jquery from "jquery";
import jquery from "jquery";
// 注意使用bt还需要同时引入：jquery与popper.js
// 引入bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.js";
// 引入element ui
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "element-ui/lib/theme-chalk/index.css";
// 引入echarts
import "echarts";
// 引入moment
// import moment from "vue-moment";
import moment from "moment";

Vue.config.productionTip = false;
Vue.use(ElementUI);
// Vue.use(moment);
Vue.prototype.moment = moment;
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
