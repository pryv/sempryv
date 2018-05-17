<template>
  <v-app id="app">
    <v-toolbar color="primary" dark fixed app>
      <v-toolbar-title :to="{name:'Home'}">SemPryv</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="red" v-if="authenticated" @click="logout()">Sign-out</v-btn>
    </v-toolbar>
    <v-content fluid
               fill-height>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
import auth from "@/auth";

export default {
  data: () => ({
    drawer: null,
    authenticated: false
  }),
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
    logout() {
      auth.signOut(() => {
        this.authenticated = false;
        this.$router.push({ name: "auth" });
      });
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
