import Vue from "vue";
import Vuetify from "vuetify";
import App from "./App.vue";
import router from "./router";

import "vuetify/dist/vuetify.min.css";

Vue.use(Vuetify, {
  theme: {
    pryv: "#bd1026"
  }
});

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
