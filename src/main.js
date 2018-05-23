import Vue from "vue";
import Vuetify from "vuetify";
import App from "./App.vue";
import router from "./router";
import { i18n, momentLocales } from "./language";
import moment from "moment";

import "vuetify/dist/vuetify.min.css";
import "@mdi/font/css/materialdesignicons.css";
import "font-awesome/css/font-awesome.css";

Vue.use(Vuetify, {
  theme: {
    pryv: "#B61E24"
  }
});

Vue.config.productionTip = false;

router.afterEach(to => {
  i18n.locale = to.params.lang;
  moment.locale(momentLocales[to.params.lang]);
});

// Create a bus for global events
var busVue = new Vue();

Object.defineProperties(Vue.prototype, {
  $bus: {
    get: function() {
      return busVue;
    }
  },
  $language: {
    get: function() {
      return i18n;
    }
  }
});

new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount("#app");
