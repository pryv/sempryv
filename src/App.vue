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
