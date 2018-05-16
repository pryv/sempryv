<template>
  <v-app id="app">
    <v-toolbar color="primary" dark fixed app>
      <v-toolbar-title :to="{name:'Home'}">SemPryv</v-toolbar-title>
    </v-toolbar>
    <v-content fluid
               fill-height>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    drawer: null
  })
};
</script>


<style>
@import url("https://fonts.googleapis.com/css?family=Exo");

#app {
  font-family: "Exo", sans-serif;
}
</style>
