import Vue from "vue";

import App from "./App.vue";

import router from "./router";
import store from "./store/index";

// import jquery from "jquery";
import jquery from "jquery"
// 注意使用bt还需要同时引入：jquery与popper.js
// 引入bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.js";
// 引入element ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import 'element-ui/lib/theme-chalk/index.css';
// 引入echarts
import "echarts";

Vue.config.productionTip = false;
Vue.use(ElementUI);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
