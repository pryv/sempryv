<template>
  <v-app id="app" fixed app>
    <infoDrawer
      ref="infoDrawer"
      v-if="authenticated"></infoDrawer>
    <MainDrawer
      ref="mainDrawer"
      v-if="authenticated"></MainDrawer>
    <v-toolbar color="primary" dark fixed clipped-left clipped-right app>
      <v-toolbar-side-icon
        @click="$refs.mainDrawer.toggle()"></v-toolbar-side-icon>
      <v-toolbar-title>SemPryv</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-menu offset-y>
          <v-btn
            flat
            slot="activator"
            dark>
            {{ get_lang() }}
            <v-icon>arrow_drop_down</v-icon>
            </v-btn>
          <v-list >
            <v-list-tile @click="set_lang('en')">
              <v-list-tile-title>EN</v-list-tile-title>
            </v-list-tile>
            <v-list-tile @click="set_lang('fr')">
              <v-list-tile-title>FR</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
        <v-btn
          flat
          v-if="authenticated"
          @click.stop="$refs.infoDrawer.toggle()">
          <v-icon>account_circle</v-icon>&nbsp;{{username}}</v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
import auth from "@/auth";
import InfoDrawer from "@/components/InfoDrawer";
import MainDrawer from "@/components/MainDrawer";

export default {
  components: {
    InfoDrawer,
    MainDrawer
  },
  data: () => ({
    authenticated: false
  }),
  computed: {
    username: function() {
      return localStorage.getItem("username");
    }
  },
  mounted() {
    this.checkAuth();
    this.$router.afterEach(() => {
      this.checkAuth();
    });
  },
  methods: {
    checkAuth() {
      auth.isConnected(
        () => {
          this.authenticated = true;
        },
        () => {
          this.authenticated = false;
          this.$router.push({ name: "auth" });
        }
      );
    },
    set_lang: function(lang) {
      const route = Object.assign({}, this.$route);
      route.params.lang = lang;
      this.$router.push(route);
    },
    get_lang: function() {
      return this.$language.locale.toUpperCase();
    }
  }
};
</script>


<style>
@import url("https://fonts.googleapis.com/css?family=Exo");

#app {
  font-family: "Exo", sans-serif;
}
</style>
