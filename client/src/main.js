import Vue from "vue";
import "@mdi/font/css/materialdesignicons.min.css";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
Vue.use(Buefy);

import App from "./App.vue";

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
}).$mount("#app");
