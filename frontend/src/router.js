import Vue from "vue";
import Router from "vue-router";
import Auth from "./views/Auth.vue";
import Home from "./views/Home.vue";
import Stream from "./views/Stream.vue";
import Event from "./views/Event.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/:lang/",
      name: "home",
      component: Home
    },
    {
      path: "/:lang/auth",
      name: "auth",
      component: Auth
    },
    {
      path: "/:lang/streams/:id",
      name: "stream",
      component: Stream
    },
    {
      path: "/:lang/events/:id",
      name: "event",
      component: Event
    },
    {
      path: "*",
      redirect: "/en/"
    }
  ]
});
